"""SONGIO card generator (HTML/CSS -> PNG/JPG via headless Chrome).
Usage: python3 make_cards_html.py cards.json out_dir
cards.json: list of {"file":"s1.jpg","kind":"cover|content|cta","theme":"pink|cyan|amber|violet|green",
 "badge":"...","title":"Текст с <em>акцентом</em>","sub":"...","step":"1/5"}
"""
import json, os, subprocess, sys, html, tempfile

W, H = 1080, 1350
THEMES = {
 "pink":   ("#ff3cac", "#784ba0", "#2b0b4d", "#12062b"),
 "cyan":   ("#2de2ff", "#3a7bd5", "#06284a", "#030f24"),
 "amber":  ("#ffb347", "#ff5e62", "#4a1408", "#1f0705"),
 "violet": ("#a78bfa", "#6d5dfc", "#1e1458", "#0b0826"),
 "green":  ("#4ade80", "#14b8a6", "#06382f", "#02150f"),
}

def page(c):
    a, b, bg1, bg2 = THEMES[c.get("theme", "pink")]
    kind = c.get("kind", "content")
    size = {"cover": 128, "content": 110, "cta": 118}[kind]
    badge = f'<div class="badge">{html.escape(c["badge"])}</div>' if c.get("badge") else ""
    step = f'<div class="step">{html.escape(c["step"])}</div>' if c.get("step") else ""
    sub = f'<p class="sub">{c["sub"]}</p>' if c.get("sub") else ""
    btn = '<div class="btn">songio.ru &nbsp;→</div>' if kind == "cta" else ""
    bars = "".join(f'<i style="height:{h}px;animation:none"></i>' for h in
        [70,150,230,120,300,200,360,240,150,320,210,120,260,180,90,230,140,70])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;height:{H}px;overflow:hidden;font-family:'Inter Display','Inter','DejaVu Sans',sans-serif;
 background:radial-gradient(1100px 900px at 85% 10%, {bg1} 0%, {bg2} 70%);color:#fff;position:relative}}
.glow{{position:absolute;width:760px;height:760px;border-radius:50%;filter:blur(120px);opacity:.55;
 background:linear-gradient(135deg,{a},{b});right:-260px;top:-220px}}
.glow2{{position:absolute;width:620px;height:620px;border-radius:50%;filter:blur(130px);opacity:.35;
 background:linear-gradient(135deg,{b},{a});left:-260px;bottom:-200px}}
.wrap{{position:absolute;inset:0;padding:84px 78px}}
.logo{{font-weight:800;font-size:38px;letter-spacing:.5px}}
.logo span{{color:{a}}}
.badge{{display:inline-block;margin-top:58px;padding:16px 34px;border-radius:60px;font-weight:800;font-size:32px;
 color:#0d0820;background:linear-gradient(90deg,{a},{b});transform:rotate(-2deg);box-shadow:0 12px 40px {a}66}}
h1{{margin-top:44px;font-weight:900;font-size:{size}px;line-height:1.02;letter-spacing:-2px;text-shadow:0 6px 40px #0008}}
h1 em{{font-style:normal;color:{a};text-shadow:0 0 36px {a}88,0 6px 40px #0008}}
.sub{{margin-top:36px;font-size:46px;line-height:1.3;color:#d9d6ee;font-weight:500;max-width:900px}}
.sub b{{color:#fff}}
.bars{{position:absolute;left:78px;right:78px;bottom:84px;height:380px;display:flex;align-items:flex-end;gap:16px}}
.bars i{{flex:1;border-radius:20px;background:linear-gradient(180deg,{a},{b});opacity:.9;box-shadow:0 0 30px {a}55}}
.step{{position:absolute;right:78px;top:88px;font-weight:700;font-size:32px;color:#ffffff99}}
.btn{{margin-top:56px;display:inline-block;padding:30px 56px;border-radius:70px;font-weight:800;font-size:50px;
 color:#0d0820;background:linear-gradient(90deg,{a},{b});box-shadow:0 18px 60px {a}77}}
</style></head><body><div class="glow"></div><div class="glow2"></div>
<div class="wrap"><div class="logo">SONGIO<span>.ru</span></div>{step}{badge}
<h1>{c["title"]}</h1>{sub}{btn}</div>
<div class="bars">{bars}</div></body></html>"""

def render(cards, out):
    os.makedirs(out, exist_ok=True)
    for c in cards:
        with tempfile.TemporaryDirectory() as td:
            hp = os.path.join(td, "c.html"); png = os.path.join(td, "c.png")
            open(hp, "w", encoding="utf-8").write(page(c))
            subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                f"--window-size={W},{H}", f"--screenshot={png}", "--force-device-scale-factor=1", "file://" + hp],
                check=True, capture_output=True, timeout=120)
            from PIL import Image
            Image.open(png).convert("RGB").crop((0, 0, W, H)).save(os.path.join(out, c["file"]), quality=93)

if __name__ == "__main__":
    render(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
