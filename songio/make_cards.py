import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350  # 4:5
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(p, s): return ImageFont.truetype(p, s)

def gradient(c1, c2):
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / H
        c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        for x in range(W):
            px[x, y] = c
    return img

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def card(name, bg, accent, tag, title, sub, idx=None):
    img = gradient(*bg)
    d = ImageDraw.Draw(img)
    # decorative equalizer bars
    import random; random.seed(name)
    for i in range(24):
        h = random.randint(60, 380)
        x = 60 + i * 41
        d.rounded_rectangle([x, H - 90 - h, x + 22, H - 90], 11, fill=accent + (0,) if False else accent)
    d.rectangle([0, 0, W, H], outline=None)
    d.text((70, 80), "SONGIO.ru", font=font(BOLD, 40), fill="white")
    d.rounded_rectangle([70, 170, 70 + d.textlength(tag, font=font(BOLD, 34)) + 50, 235], 32, fill=accent)
    d.text((95, 180), tag, font=font(BOLD, 34), fill=(15, 15, 25))
    f = font(BOLD, 96)
    y = 330
    for ln in wrap(d, title, f, W - 140):
        d.text((70, y), ln, font=f, fill="white"); y += 118
    f2 = font(REG, 44)
    y += 20
    for ln in wrap(d, sub, f2, W - 140):
        d.text((70, y), ln, font=f2, fill=(220, 220, 235)); y += 62
    img.save(name, quality=95)

dark = ((20, 12, 45), (70, 20, 110))
cards = [
 ("slide1.jpg", dark, (255, 80, 200), "ЭКСПЕРИМЕНТ", "Один текст. Пять жанров.", "Пишем одну песню — и смотрим, как она звучит в разных стилях"),
 ("slide2.jpg", ((40,10,20),(150,30,50)), (255,170,60), "РОК", "Тот же текст, но с гитарами", "Драйв, живые барабаны, надрывный вокал"),
 ("slide3.jpg", ((10,25,45),(20,90,120)), (80,230,255), "ДЖАЗ", "Тот же текст, но в баре", "Саксофон, контрабас и мягкий голос"),
 ("slide4.jpg", ((45,15,10),(160,60,20)), (255,210,80), "ФЛАМЕНКО", "Тот же текст, но со страстью", "Гитара, хлопки, испанский темперамент"),
 ("slide5.jpg", ((10,10,30),(40,20,120)), (140,120,255), "ЭЛЕКТРОНИКА", "Тот же текст, но на танцполе", "Синтезаторы, бас и ритм до утра"),
 ("slide6.jpg", dark, (255, 80, 200), "ПОПРОБУЙ САМ", "Первая песня — бесплатно", "Опиши идею на songio.ru — трек будет готов через ~2 минуты"),
]
for c in cards: card(*c)
