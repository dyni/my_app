"""SONGIO infographic cards v2 (glass / bento / diagrams), 1080x1350 JPG via headless Chrome.
Usage: python3 make_infographics.py out_dir [series ...]   (series: fast intro cat)
Slides are defined in SERIES at the bottom; each is (file, theme, builder-html)."""
import os, random, subprocess, sys, tempfile, hashlib

W, H = 1080, 1350
THEMES = {  # accent1, accent2, bg-glow1, bg-glow2
 "pink":   ("#ff4fb8", "#8b5cf6", "#5b1d7a", "#1a0838"),
 "cyan":   ("#2de2ff", "#4f7cff", "#0e4d86", "#06122b"),
 "amber":  ("#ffc247", "#ff5e62", "#7a2a10", "#1f0a06"),
 "violet": ("#b39dff", "#6d5dfc", "#352a9c", "#0c0929"),
 "green":  ("#4ff0a0", "#14b8c6", "#0b5a49", "#031712"),
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1350px;overflow:hidden;position:relative;color:#fff;
 font-family:'Inter Display','Inter','DejaVu Sans',sans-serif;background:#07060f}
.bg{position:absolute;inset:0;background:
 radial-gradient(900px 700px at 100% 0%,var(--g1) 0%,transparent 70%),
 radial-gradient(800px 700px at 0% 100%,var(--g1) 0%,transparent 70%),
 linear-gradient(180deg,var(--g2),#06050d)}
.dots{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.09) 2px,transparent 2px);background-size:54px 54px;
 -webkit-mask-image:linear-gradient(180deg,transparent,#000 40%,transparent);mask-image:linear-gradient(180deg,transparent,#000 40%,transparent)}
.wrap{position:absolute;inset:0;padding:70px 72px 60px;display:flex;flex-direction:column;z-index:3}
.top{display:flex;justify-content:space-between;align-items:center}
.logo{font-weight:800;font-size:36px;letter-spacing:.5px;display:flex;align-items:center;gap:12px}
.logo i{width:16px;height:16px;border-radius:50%;background:linear-gradient(135deg,var(--a),var(--b));box-shadow:0 0 22px var(--a)}
.logo span{color:var(--a)}
.pg{font-weight:700;font-size:26px;padding:10px 22px;border-radius:40px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.16)}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px;min-height:0}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:600;color:rgba(255,255,255,.55)}
.foot b{color:#fff;font-weight:700}
h1{font-weight:800;font-size:104px;line-height:1.02;letter-spacing:-3px}
h1.m{font-size:88px;letter-spacing:-2.5px}
h1 em,.g{font-style:normal;background:linear-gradient(90deg,var(--a),var(--b));-webkit-background-clip:text;background-clip:text;color:transparent}
.lead{font-size:38px;line-height:1.3;color:rgba(255,255,255,.78);font-weight:500}
.lead b{color:#fff}
.glass{background:linear-gradient(160deg,rgba(255,255,255,.12),rgba(255,255,255,.04));border:1.5px solid rgba(255,255,255,.18);
 border-radius:40px;box-shadow:0 30px 80px rgba(0,0,0,.35)}
.pill{display:inline-flex;align-items:center;gap:12px;padding:14px 30px;border-radius:60px;font-weight:800;font-size:30px;
 color:#0b0820;background:linear-gradient(90deg,var(--a),var(--b));align-self:flex-start;box-shadow:0 12px 40px color-mix(in srgb,var(--a) 45%,transparent)}
.chip{display:inline-block;padding:16px 30px;border-radius:60px;font-size:34px;font-weight:700;background:rgba(255,255,255,.09);border:1.5px solid rgba(255,255,255,.2)}
.chip.on{background:linear-gradient(90deg,var(--a),var(--b));color:#0b0820;border-color:transparent}
.btn{align-self:flex-start;padding:26px 52px;border-radius:70px;font-weight:800;font-size:44px;color:#0b0820;
 background:linear-gradient(90deg,var(--a),var(--b));box-shadow:0 18px 60px color-mix(in srgb,var(--a) 55%,transparent)}
/* player */
.player{padding:30px;display:flex;align-items:center;gap:28px}
.art{width:128px;height:128px;border-radius:30px;flex:none;background:linear-gradient(135deg,var(--a),var(--b));
 display:flex;align-items:center;justify-content:center;font-size:62px;color:#0b0820;font-weight:800}
.pl-b{flex:1;min-width:0}
.pl-t{font-size:32px;font-weight:800;margin-bottom:6px}
.pl-s{font-size:26px;color:rgba(255,255,255,.6);font-weight:600;margin-bottom:14px}
.wave{display:flex;align-items:center;gap:5px;height:64px}
.wave i{flex:1;border-radius:4px;background:rgba(255,255,255,.28);min-width:3px}
.wave i.on{background:linear-gradient(180deg,var(--a),var(--b))}
.play{width:84px;height:84px;border-radius:50%;flex:none;background:#fff;display:flex;align-items:center;justify-content:center}
.play:after{content:"";border-left:28px solid #0b0820;border-top:17px solid transparent;border-bottom:17px solid transparent;margin-left:8px}
.tag{display:inline-block;font-size:24px;font-weight:800;padding:8px 18px;border-radius:14px;background:rgba(255,255,255,.14);margin-bottom:10px;letter-spacing:.5px}
/* steps */
.steps{position:relative;display:flex;flex-direction:column;gap:30px}
.steps:before{content:"";position:absolute;left:61px;top:80px;bottom:80px;width:5px;border-radius:4px;background:linear-gradient(180deg,var(--a),var(--b));opacity:.55}
.step{display:flex;gap:34px;align-items:center;padding:34px 38px;position:relative}
.num{width:90px;height:90px;border-radius:28px;flex:none;background:linear-gradient(135deg,var(--a),var(--b));color:#0b0820;
 font-weight:800;font-size:44px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 36px color-mix(in srgb,var(--a) 50%,transparent)}
.st-t{font-size:48px;font-weight:800;letter-spacing:-1px;margin-bottom:6px}
.st-s{font-size:30px;color:rgba(255,255,255,.68);font-weight:500;line-height:1.25}
/* bento */
.bento{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.tile{padding:40px 38px;display:flex;flex-direction:column;justify-content:space-between;min-height:290px}
.tile.w{grid-column:span 2;min-height:220px}
.big{font-size:128px;font-weight:800;letter-spacing:-5px;line-height:1}
.tl{font-size:32px;font-weight:600;color:rgba(255,255,255,.72);line-height:1.25;margin-top:14px}
.tl b{color:#fff}
.cloud{display:flex;flex-wrap:wrap;gap:20px}
.arrow{align-self:center;width:0;height:0;border-left:30px solid transparent;border-right:30px solid transparent;border-top:42px solid var(--a);opacity:.9}
.pm{padding:38px 42px;font-size:44px;line-height:1.38;font-weight:600}
.pm .k{padding:2px 14px;border-radius:14px;font-weight:700}
.k1{background:color-mix(in srgb,#ffc247 38%,transparent)}.k2{background:color-mix(in srgb,#ff4fb8 38%,transparent)}
.k3{background:color-mix(in srgb,#2de2ff 38%,transparent)}.k4{background:color-mix(in srgb,#4ff0a0 38%,transparent)}
.leg{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.leg div{display:flex;align-items:center;gap:18px;font-size:34px;font-weight:700}
.leg s{display:block;width:34px;height:34px;border-radius:11px;flex:none;text-decoration:none}
.vs{display:flex;flex-direction:column;gap:26px}
.vs .glass{padding:36px 40px}
.vs .lab{font-size:26px;font-weight:800;letter-spacing:1px;margin-bottom:12px}
.vs .tx{font-size:40px;font-weight:600;line-height:1.3}
.vs .bad .lab{color:#ff8a8a}.vs .good .lab{color:var(--a)}
.vs .good{border-color:var(--a);box-shadow:0 0 0 2px var(--a),0 30px 80px rgba(0,0,0,.35)}
/* timeline (video) */
.tlr{padding:34px;display:flex;flex-direction:column;gap:18px}
.row{display:flex;gap:12px;height:96px}
.clip{border-radius:20px;flex:1;display:flex;align-items:center;padding:0 22px;font-size:26px;font-weight:700;color:#0b0820}
.audio{height:150px;border-radius:24px;border:2px dashed var(--a);padding:0 24px;display:flex;align-items:center;background:rgba(255,255,255,.05)}
.audio .wave{width:100%;height:96px}
.rl{font-size:24px;font-weight:700;color:rgba(255,255,255,.6);letter-spacing:1px}
"""

def wave(seed, n=34, on=0.55):
    r = random.Random(seed); out = ""
    for k in range(n):
        h = int(14 + 50 * abs(__import__("math").sin(k * .42 + r.random())) ** .8 * r.uniform(.6, 1))
        out += f'<i class="{"on" if k < n*on else ""}" style="height:{h}px"></i>'
    return f'<div class="wave">{out}</div>'

def player(name, sub, seed, icon="♪", on=.55):
    return (f'<div class="glass player"><div class="art">{icon}</div><div class="pl-b"><div class="pl-t">{name}</div>'
            f'<div class="pl-s">{sub}</div>{wave(seed, on=on)}</div><div class="play"></div></div>')

def frame(theme, pg, body, last=False):
    a, b, g1, g2 = THEMES[theme]
    hint = '<span>Листай <b>→</b></span>' if not last else '<span></span>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{--a:{a};--b:{b};--g1:{g1};--g2:{g2}}}{CSS}</style></head>
<body><div class="bg"></div><div class="dots"></div><div class="wrap">
<div class="top"><div class="logo"><i></i><u style="text-decoration:none">SONGIO<span>.ru</span></u></div>{f'<div class="pg">{pg}</div>' if pg else ''}</div>
<div class="main">{body}</div>
<div class="foot">{hint}<span>songio<b>.ru</b></span></div></div></body></html>"""

def cta(title, sub):
    return f'<h1 class="m">{title}</h1><p class="lead">{sub}</p><div class="btn">songio.ru &nbsp;→</div>'

# ---------------------------------------------------------------- series
def S_fast():
    return [
     ("fast1.jpg", "violet", "1/5", False,
      '<div class="pill">● БЕСПЛАТНО</div><h1>Песня <em>за 2 минуты</em></h1><p class="lead">Опиши идею — получи готовый трек на русском</p>'
      + player("Твоя песня", "Версия A · 2:00", 11, "♪", .45)
      + '<div style="margin-top:-6px">' + player("Твоя песня", "Версия B · 2:00", 12, "♫", .2) + '</div>'),
     ("fast2.jpg", "pink", "2/5", False,
      '<h1 class="m">Как это <em>работает</em></h1><div class="steps">'
      '<div class="glass step"><div class="num">1</div><div><div class="st-t">Опиши идею</div><div class="st-s">О чём песня и для кого. Или вставь свой текст</div></div></div>'
      '<div class="glass step"><div class="num">2</div><div><div class="st-t">Выбери стиль и голос</div><div class="st-s">60+ стилей: от рока до фламенко</div></div></div>'
      '<div class="glass step"><div class="num">3</div><div><div class="st-t">Получи 2 версии</div><div class="st-s">Трек готов примерно через 2 минуты</div></div></div></div>'),
     ("fast3.jpg", "cyan", "3/5", False,
      '<h1 class="m"><em>60+</em> стилей на любое настроение</h1><div class="cloud">'
      + "".join(f'<span class="chip{" on" if i in (0,4,7) else ""}">{t}</span>' for i, t in enumerate(
        ["поп","рок","джаз","фолк","EDM","фламенко","лирика","акустика","электроника","блюз","шансон","рэп"]))
      + '</div><p class="lead">А ещё — разные голоса: женский, мужской и не только</p>'),
     ("fast4.jpg", "green", "4/5", False,
      '<h1 class="m">SONGIO <em>в цифрах</em></h1><div class="bento">'
      '<div class="glass tile"><div class="big g">2</div><div class="tl"><b>минуты</b> до готового трека</div></div>'
      '<div class="glass tile"><div class="big g">×2</div><div class="tl"><b>версии</b> за каждую генерацию</div></div>'
      '<div class="glass tile"><div class="big g">60+</div><div class="tl"><b>стилей</b> и жанров</div></div>'
      '<div class="glass tile"><div class="big g" style="font-size:84px;letter-spacing:-3px;padding-top:22px">Бесплатно</div><div class="tl">первая демо-генерация, <b>без карты</b></div></div></div>'),
     ("fast5.jpg", "violet", "5/5", True,
      cta("Первая песня <em>бесплатно</em>", "Без карты и подписок. Есть и <b>Telegram-бот</b>")
      + player("Твоя идея", "Версия A · ждёт тебя", 21, "♪", .0)),
    ]

def S_intro():
    clipcols = ["#4ff0a0", "#2de2ff", "#ffc247", "#ff8fd0"]
    clips = "".join(f'<div class="clip" style="background:{c}">{t}</div>' for c, t in zip(clipcols, ["Интро", "Сцена 1", "Сцена 2", "Финал"]))
    return [
     ("intro1.jpg", "green", "1/4", False,
      '<div class="pill">АВТОРАМ И БЛОГЕРАМ</div><h1>Свой звук <em>для канала</em></h1>'
      '<div class="glass tlr"><div class="rl">ВИДЕО</div><div class="row">' + clips + '</div>'
      '<div class="rl">ТВОЙ ТРЕК</div><div class="audio">' + wave(5, 44, .0).replace('class=""', 'class="on"') + '</div></div>'
      '<p class="lead">Интро и заставка <b>без поиска по стокам</b></p>'),
     ("intro2.jpg", "cyan", "2/4", False,
      '<h1 class="m">Идея → <em>трек</em></h1>'
      '<div class="glass pm"><span class="tag">ТВОЙ ЗАПРОС</span><br>Энергичное <span class="k k1">интро для подкаста</span> про стартапы, <span class="k k3">электроника</span>, <span class="k k4">без вокала</span></div>'
      '<div class="arrow"></div>'
      + player("Интро для подкаста", "Версия A · готово", 31, "♪", .6)
      + '<div style="margin-top:-8px">' + player("Интро для подкаста", "Версия B · готово", 32, "♫", .3) + '</div>'),
     ("intro3.jpg", "amber", "3/4", False,
      '<h1 class="m">Где <em>пригодится</em></h1><div class="bento">'
      '<div class="glass tile"><div class="big" style="font-size:90px">🎙</div><div class="tl"><b>Подкасты</b><br>интро и заставки</div></div>'
      '<div class="glass tile"><div class="big" style="font-size:90px">📱</div><div class="tl"><b>Рилс и сторис</b><br>свой трек в кадре</div></div>'
      '<div class="glass tile"><div class="big" style="font-size:90px">▶</div><div class="tl"><b>YouTube</b><br>музыка для роликов</div></div>'
      '<div class="glass tile"><div class="big" style="font-size:90px">★</div><div class="tl"><b>Бренд</b><br>узнаваемый джингл</div></div></div>'),
     ("intro4.jpg", "green", "4/4", True,
      cta("Сделай звук <em>своим</em>", "Первая демо-генерация бесплатно, без карты")),
    ]

def S_cat():
    return [
     ("cat1.jpg", "amber", "1/4", False,
      '<div class="pill">ПРОМПТ → РЕЗУЛЬТАТ</div><h1>Идея → <em>хит про кота</em></h1>'
      '<div class="glass pm" style="font-size:40px"><span class="tag">ТЫ ПИШЕШЬ</span><br>Смешная песня про кота, который ненавидит понедельники, рок-н-ролл, мужской голос</div>'
      '<div class="arrow"></div>' + player("Кот против понедельника", "Рок-н-ролл · 2:00", 41, "🐱", .4)),
     ("cat2.jpg", "pink", "2/4", False,
      '<h1 class="m">Из чего <em>состоит</em> хорошая идея</h1>'
      '<div class="glass pm"><span class="k k1">Герой:</span> кот, который ненавидит понедельники. <span class="k k2">Тон:</span> смешная песня. <span class="k k3">Жанр:</span> рок-н-ролл. <span class="k k4">Голос:</span> мужской</div>'
      '<div class="leg"><div><s style="background:#ffc247"></s>Герой</div><div><s style="background:#ff4fb8"></s>Тон</div>'
      '<div><s style="background:#2de2ff"></s>Жанр</div><div><s style="background:#4ff0a0"></s>Голос</div></div>'),
     ("cat3.jpg", "cyan", "3/4", False,
      '<h1 class="m">Размыто <em>vs</em> конкретно</h1><div class="vs">'
      '<div class="glass bad"><div class="lab">✕ РАЗМЫТО</div><div class="tx">Песня про кота</div></div>'
      '<div class="glass good"><div class="lab">✓ КОНКРЕТНО</div><div class="tx">Смешная песня про кота, который ненавидит понедельники, рок-н-ролл, мужской голос</div></div></div>'
      '<p class="lead">Чем точнее описание, тем ближе трек к твоей идее</p>'),
     ("cat4.jpg", "amber", "4/4", True,
      cta("Что споёшь <em>ты</em>?", "Первая демо-генерация бесплатно, без карты. Каждый раз — <b>2 версии</b>")),
    ]

SERIES = {"fast": S_fast, "intro": S_intro, "cat": S_cat}

def render(out, names):
    from PIL import Image
    os.makedirs(out, exist_ok=True)
    for n in names:
        for fn, theme, pg, last, body in SERIES[n]():
            with tempfile.TemporaryDirectory() as td:
                hp, png = os.path.join(td, "c.html"), os.path.join(td, "c.png")
                open(hp, "w", encoding="utf-8").write(frame(theme, pg, body, last))
                subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={W},{H}", f"--screenshot={png}", "--force-device-scale-factor=1", "file://" + hp],
                    check=True, capture_output=True, timeout=120)
                Image.open(png).convert("RGB").crop((0, 0, W, H)).save(os.path.join(out, fn), quality=93)

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2:] or list(SERIES))
