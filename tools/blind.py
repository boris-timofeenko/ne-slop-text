"""Слепой тест для любых текстов: ранжирование без повторов + пометки «слоп / живое» по предложениям.

usage: blind.py OUT.html KEY.json "Заголовок" "Подзаголовок" name=path[=метка] ... [--raw]
Текст: абзацы через пустую строку; строки «- » — пункты списка. Порядок вариантов перемешивается, ключ пишется в KEY.json
и в код страницы (кнопка «Раскрыть»). Результат собирается кнопкой и копируется в буфер.

Типографика выравнивается у всех вариантов (кавычки прямые, длинное и среднее тире -> « - »): иначе один вариант
выдаёт себя оформлением. В одном тесте оригинал человека был единственным с длинным тире, и судья, приученный считать
тире признаком ИИ, поставил его последним. --raw отключает выравнивание.
"""
import html, json, random, re, sys, time

RAW = "--raw" in sys.argv
out, keyfile, title, subtitle, *items = [a for a in sys.argv[1:] if a != "--raw"]


def typography(t):
    if RAW:
        return t
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s*[—–]\s*", " - ", t)
variants = []
for it in items:
    parts = it.split("=", 2)
    variants.append((parts[0], parts[1], parts[2] if len(parts) > 2 else parts[0]))
random.seed(time.time_ns()); random.shuffle(variants)
letters = "ABCDEFGHIJ"[:len(variants)]
sid = 0

def spans(text, L):
    global sid
    out = []
    for p in re.split(r"(?<=[.;!?])\s+(?=[A-Z0-9~\"“(])", text.strip()):
        sid += 1
        out.append(f'<span class="s" data-v="{L}" data-id="{L}{sid}">{html.escape(p)}</span>')
    return " ".join(out)

def render(text, L):
    blocks, h = re.split(r"\n\s*\n", text.strip()), []
    for b in blocks:
        lines = [l.strip() for l in b.splitlines() if l.strip()]
        if all(l.startswith("- ") for l in lines):
            h.append("<ul>" + "".join(f"<li>{spans(l[2:], L)}</li>" for l in lines) + "</ul>")
        else:
            h.append(f"<p>{spans(' '.join(lines), L)}</p>")
    return "\n".join(h)

sheets, key = [], {}
n = len(variants)
for L, (name, path, label) in zip(letters, variants):
    key[L] = {"name": name, "label": label}
    sheets.append(f'''<section class="sheet"><div class="rail">{L}</div><div class="body">
{render(typography(open(path).read()), L)}
<div class="rate"><span class="lbl">Место (1 = лучше всех)</span><span class="stars" data-v="{L}">{"".join(f'<button data-n="{i}">{i}</button>' for i in range(1, n + 1))}</span>
<textarea data-v="{L}" placeholder="Что режет глаз, что живое (необязательно)"></textarea></div></div></section>''')
json.dump(key, open(keyfile, "w"), ensure_ascii=False, indent=1)
store = "blind-" + re.sub(r"\W+", "-", out)[-40:]
page = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><style>
:root{{--olive:#4E5A24;--ink:#1A1C17;--body:#2B2E27;--muted:#6E7266;--desk:#E9E7E0;--slopbg:#F6DEDB;--slop:#B3261E;--livebg:#DDEBD8}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--desk);color:var(--body);font:15px/1.55 Charter,"Iowan Old Style",Georgia,serif}}
header,footer{{max-width:820px;margin:0 auto;padding:24px 16px 4px;font-family:-apple-system,"Helvetica Neue",Arial,sans-serif}}
h1{{font-size:20px;margin:0 0 6px;color:var(--ink)}} header p{{margin:4px 0;font-size:14px}}
.sheet{{max-width:820px;margin:16px auto;background:#fff;display:flex;box-shadow:0 1px 2px rgba(0,0,0,.12)}}
.rail{{width:56px;flex:none;text-align:right;padding:20px 12px 0 0;color:var(--olive);font:700 26px/1 -apple-system,Arial,sans-serif}}
.body{{flex:1;min-width:0;padding:18px 26px 20px 4px}} p{{margin:0 0 10px}} ul{{margin:0 0 10px;padding-left:18px}}
.s{{cursor:pointer;border-radius:2px}} .s:hover{{background:#F1EFE6}}
.s.slop{{background:var(--slopbg);text-decoration:underline wavy var(--slop);text-decoration-thickness:1px;text-underline-offset:3px}} .s.live{{background:var(--livebg)}}
.rate{{margin-top:14px;padding-top:12px;border-top:1px solid #E4E2DA;display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;font-family:-apple-system,Arial,sans-serif}}
.lbl{{color:var(--olive);font-weight:700;font-size:12px;text-transform:uppercase}}
.stars button{{width:34px;height:30px;border:1px solid #C9C6BA;background:#fff;color:var(--ink);font-size:14px;cursor:pointer;margin-right:-1px}}
.stars button.on{{background:var(--olive);color:#fff;border-color:var(--olive)}}
textarea{{flex:1 1 100%;min-height:42px;border:1px solid #D6D3C8;padding:6px 8px;font:14px -apple-system,Arial,sans-serif}}
footer button{{font-size:14px;padding:8px 14px;border:1px solid var(--olive);background:var(--olive);color:#fff;cursor:pointer;margin:0 8px 8px 0}}
footer .ghost{{background:transparent;color:var(--olive)}} #out{{display:none;width:100%;min-height:160px;font:13px/1.4 ui-monospace,Menlo,monospace}} #key{{display:none;background:#fff;padding:12px 16px}}
@media (max-width:600px){{.rail{{width:32px;padding-right:8px;font-size:20px}} .body{{padding:14px 14px 16px 2px}}}}
</style></head><body>
<header><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p>
<p>Клик по предложению: первый — <span style="background:var(--slopbg)">слоп</span>, второй — <span style="background:var(--livebg)">живое</span>, третий — снять. Места 1–{n} без повторов. В конце «Собрать результат» и вставь текст в чат.</p></header>
{"".join(sheets)}
<footer><button id="collect">Собрать результат</button><button id="reveal" class="ghost">Раскрыть варианты</button>
<textarea id="out" readonly></textarea><div id="key"></div></footer>
<script>
const KEY={json.dumps({k: v["label"] for k, v in key.items()}, ensure_ascii=False)}; const STORE={json.dumps(store)};
let st={{marks:{{}},rate:{{}},note:{{}}}}; try{{const r=localStorage.getItem(STORE); if(r) st=Object.assign(st,JSON.parse(r));}}catch(e){{}}
const save=()=>{{try{{localStorage.setItem(STORE,JSON.stringify(st));}}catch(e){{}}}};
const cyc={{undefined:"slop",slop:"live",live:undefined}};
document.querySelectorAll(".s").forEach(el=>{{const id=el.dataset.id; if(st.marks[id]) el.classList.add(st.marks[id]);
 el.onclick=()=>{{const n=cyc[st.marks[id]]; el.classList.remove("slop","live"); if(n){{st.marks[id]=n; el.classList.add(n);}} else delete st.marks[id]; save();}};}});
const paintAll=()=>document.querySelectorAll(".stars").forEach(b=>b.querySelectorAll("button").forEach(x=>x.classList.toggle("on",+x.dataset.n===st.rate[b.dataset.v])));
document.querySelectorAll(".stars button").forEach(b=>b.onclick=()=>{{const v=b.parentNode.dataset.v,n=+b.dataset.n; for(const k in st.rate) if(k!==v&&st.rate[k]===n) delete st.rate[k]; st.rate[v]=n; paintAll(); save();}});
paintAll();
document.querySelectorAll("textarea[data-v]").forEach(t=>{{t.value=st.note[t.dataset.v]||""; t.oninput=()=>{{st.note[t.dataset.v]=t.value; save();}};}});
document.getElementById("collect").onclick=()=>{{const L=[]; Object.keys(KEY).forEach(v=>{{L.push(`## ${{v}}: место ${{st.rate[v]||"—"}}`+(st.note[v]?` — ${{st.note[v].trim()}}`:""));
 document.querySelectorAll(`.s[data-v="${{v}}"]`).forEach(el=>{{const m=st.marks[el.dataset.id]; if(m) L.push(`${{m==="slop"?"[слоп]":"[живое]"}} ${{el.textContent}}`);}});}});
 const o=document.getElementById("out"); o.style.display="block"; o.value=L.join("\\n"); o.select(); try{{navigator.clipboard.writeText(o.value);}}catch(e){{}}}};
document.getElementById("reveal").onclick=()=>{{if(!confirm("Раскрыть, какой вариант чей? Лучше после оценки.")) return; const k=document.getElementById("key"); k.style.display="block";
 k.innerHTML=Object.entries(KEY).map(([l,n])=>`<div><b>${{l}}</b> — ${{n}}</div>`).join("");}};
</script></body></html>'''
open(out, "w").write(page)
print({k: v["name"] for k, v in key.items()})
