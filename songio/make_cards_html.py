"""SONGIO card generator (HTML/CSS -> JPG via headless Chrome), 1080x1350.
Usage: python3 make_cards_html.py cards.json out_dir
cards.json: list of objects:
 file   : "s1.jpg"
 kind   : cover | content | cta          (size of headline; cta adds a button)
 theme  : pink | cyan | amber | violet | green
 layout : bars | center | bigword | chat | split | rings | grid | notes  (optional; if missing chosen from file name)
 title  : headline, use <em>accent</em> for the highlighted word(s)
 sub    : optional subline (<b> allowed)
 badge  : optional pill ("БЕСПЛАТНО")
 step   : optional "2/5"
 big    : text for layout bigword (e.g. "2:00", "60+", "×2")
 prompt : text for layout chat (what the user types)  ;  reply : optional answer bubble
Vary layout and theme between neighbouring posts so the feed does not look uniform."""
import json, os, random, subprocess, sys, html, tempfile, hashlib

W, H = 1080, 1350
THEMES = {
 "pink":   ("#ff3cac", "#784ba0", "#2b0b4d", "#12062b"),
 "cyan":   ("#2de2ff", "#3a7bd5", "#06284a", "#030f24"),
 "amber":  ("#ffb347", "#ff5e62", "#4a1408", "#1f0705"),
 "violet": ("#a78bfa", "#6d5dfc", "#1e1458", "#0b0826"),
 "green":  ("#4ade80", "#14b8a6", "#06382f", "#02150f"),
}
LAYOUTS = ["bars", "center", "bigword", "chat", "split", "rings", "grid", "notes"]

def decor(layout, rnd, a, b):
    if layout == "bars":
        n = rnd.choice([14, 18, 22]); hs = [rnd.randint(60, 380) for _ in range(n)]
        return '<div class="bars">' + "".join(f'<i style="height:{h}px"></i>' for h in hs) + '</div>'
    if layout == "rings":
        return ''.join(f'<div class="ring" style="width:{s}px;height:{s}px;right:{x}px;bottom:{y}px;opacity:{o}"></div>'
            for s, x, y, o in [(900,-250,-250,.5),(640,-120,-120,.7),(380,10,10,.9)])
    if layout == "grid":
        return '<div class="grid"></div>'
    if layout == "notes":
        out = ""
        for _ in range(9):
            ch = rnd.choice("♪♫♬𝄞"); s = rnd.randint(90, 240)
            out += f'<div class="note" style="font-size:{s}px;left:{rnd.randint(40,900)}px;top:{rnd.randint(760,1200)}px;opacity:{rnd.uniform(.12,.4):.2f};transform:rotate({rnd.randint(-25,25)}deg)">{ch}</div>'
        return out
    if layout == "split":
        return '<div class="diag"></div>'
    return ''

def page(c):
    rnd = random.Random(hashlib.md5(c["file"].encode()).hexdigest())
    a, b, bg1, bg2 = THEMES[c.get("theme", "pink")]
    kind = c.get("kind", "content")
    layout = c.get("layout") or LAYOUTS[int(hashlib.md5(c["file"].encode()).hexdigest(), 16) % len(LAYOUTS)]
    size = {"cover": 124, "content": 106, "cta": 114}[kind]
    if layout in ("center", "bigword"): size -= 14
    badge = f'<div class="badge">{html.escape(c["badge"])}</div>' if c.get("badge") else ""
    step = f'<div class="step">{html.escape(c["step"])}</div>' if c.get("step") else ""
    sub = f'<p class="sub">{c["sub"]}</p>' if c.get("sub") else ""
    btn = '<div class="btn">songio.ru &nbsp;→</div>' if kind == "cta" else ""
    big = f'<div class="bigw">{html.escape(c["big"])}</div>' if layout == "bigword" and c.get("big") else ""
    chat = ""
    if layout == "chat":
        p = html.escape(c.get("prompt", "Песня про осень, грустный джаз, женский голос"))
        chat = f'<div class="bub me">{p}</div>'
        if c.get("reply") is not False:
            chat += f'<div class="bub bot">🎵 {html.escape(c.get("reply", "Готово: 2 версии трека"))}</div>'
        chat = f'<div class="chat">{chat}</div>'
    align = "center" if layout in ("center", "bigword") else "left"
    # place for headline block
    top = {"center": 250, "bigword": 130, "split": 120}.get(layout, 0)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;height:{H}px;overflow:hidden;font-family:'Inter Display','Inter','DejaVu Sans',sans-serif;
 background:radial-gradient(1100px 900px at {rnd.choice([85,15,50])}% {rnd.choice([5,15])}%, {bg1} 0%, {bg2} 70%);color:#fff;position:relative}}
.glow{{position:absolute;width:760px;height:760px;border-radius:50%;filter:blur(120px);opacity:.5;
 background:linear-gradient(135deg,{a},{b});right:-260px;top:-220px}}
.glow2{{position:absolute;width:620px;height:620px;border-radius:50%;filter:blur(130px);opacity:.35;
 background:linear-gradient(135deg,{b},{a});left:-260px;bottom:-200px}}
.wrap{{position:absolute;inset:0;padding:84px 78px;text-align:{align};z-index:3}}
.logo{{font-weight:800;font-size:38px;letter-spacing:.5px}} .logo span{{color:{a}}}
.badge{{display:inline-block;margin-top:{'46px' if align=='center' else '58px'};padding:16px 34px;border-radius:60px;font-weight:800;font-size:32px;
 color:#0d0820;background:linear-gradient(90deg,{a},{b});transform:rotate(-2deg);box-shadow:0 12px 40px {a}66}}
.hd{{margin-top:{top}px}}
h1{{margin-top:44px;font-weight:900;font-size:{size}px;line-height:1.02;letter-spacing:-2px;text-shadow:0 6px 40px #0008}}
h1 em{{font-style:normal;color:{a};text-shadow:0 0 36px {a}88,0 6px 40px #0008}}
.sub{{margin-top:36px;font-size:46px;line-height:1.3;color:#d9d6ee;font-weight:500;{'margin-left:auto;margin-right:auto;' if align=='center' else ''}max-width:900px}}
.sub b{{color:#fff}}
.bars{{position:absolute;left:78px;right:78px;bottom:84px;height:380px;display:flex;align-items:flex-end;gap:16px;z-index:1}}
.bars i{{flex:1;border-radius:20px;background:linear-gradient(180deg,{a},{b});opacity:.9;box-shadow:0 0 30px {a}55}}
.step{{position:absolute;right:78px;top:88px;font-weight:700;font-size:32px;color:#ffffff99}}
.btn{{margin-top:56px;display:inline-block;padding:30px 56px;border-radius:70px;font-weight:800;font-size:50px;
 color:#0d0820;background:linear-gradient(90deg,{a},{b});box-shadow:0 18px 60px {a}77}}
.ring{{position:absolute;border-radius:50%;border:6px solid {a};box-shadow:0 0 60px {a}66, inset 0 0 60px {a}33;z-index:1}}
.grid{{position:absolute;inset:0;z-index:1;background-image:linear-gradient({a}22 2px,transparent 2px),linear-gradient(90deg,{a}22 2px,transparent 2px);
 background-size:90px 90px;-webkit-mask-image:linear-gradient(0deg,#000 5%,transparent 70%)}}
.note{{position:absolute;color:{a};z-index:1;text-shadow:0 0 40px {a}}}
.diag{{position:absolute;left:-200px;right:-200px;bottom:-80px;height:560px;transform:rotate(-8deg);z-index:1;
 background:linear-gradient(120deg,{a},{b});box-shadow:0 -20px 80px {a}55}}
.bigw{{margin-top:40px;font-weight:900;font-size:300px;line-height:1;letter-spacing:-8px;color:{a};text-shadow:0 0 80px {a}99}}
.chat{{margin-top:56px;display:flex;flex-direction:column;gap:22px;text-align:left}}
.bub{{max-width:820px;padding:32px 42px;font-size:42px;line-height:1.3;font-weight:600;border-radius:44px}}
.bub.me{{align-self:flex-end;background:linear-gradient(90deg,{a},{b});color:#0d0820;border-bottom-right-radius:12px}}
.bub.bot{{align-self:flex-start;background:#ffffff1c;border:2px solid #ffffff33;border-bottom-left-radius:12px;backdrop-filter:blur(8px)}}
</style></head><body><div class="glow"></div><div class="glow2"></div>
{decor(layout, rnd, a, b)}
<div class="wrap"><div class="logo">SONGIO<span>.ru</span></div>{step}
<div class="hd">{badge}{big}<h1>{c["title"]}</h1>{sub}{chat}{btn}</div></div></body></html>"""

def render(cards, out):
    from PIL import Image
    os.makedirs(out, exist_ok=True)
    for c in cards:
        with tempfile.TemporaryDirectory() as td:
            hp = os.path.join(td, "c.html"); png = os.path.join(td, "c.png")
            open(hp, "w", encoding="utf-8").write(page(c))
            subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                f"--window-size={W},{H}", f"--screenshot={png}", "--force-device-scale-factor=1", "file://" + hp],
                check=True, capture_output=True, timeout=120)
            Image.open(png).convert("RGB").crop((0, 0, W, H)).save(os.path.join(out, c["file"]), quality=93)

if __name__ == "__main__":
    render(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
