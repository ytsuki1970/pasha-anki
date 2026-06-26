# -*- coding: utf-8 -*-
# すごい暗記帳 アプリアイコン生成（PNG）。フォント非依存（図形のみ）。
import os, math
from PIL import Image, ImageDraw

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def card_layer(size, angle, fill_rgb, alpha, stripe, lines):
    cw = int(size * 0.50)
    ch = int(size * 0.58)
    rad = int(size * 0.085)
    card = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=rad, fill=(fill_rgb[0], fill_rgb[1], fill_rgb[2], 255))
    if stripe:
        sh = int(ch * 0.22)
        d.rectangle([0, 0, cw, sh], fill=(31, 195, 176, 255))  # teal
    if lines:
        lx = int(cw * 0.16); lw = int(cw * 0.68); lh = max(4, int(ch * 0.075))
        ly = int(ch * 0.44)
        d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=lh // 2, fill=(231, 222, 203, 255))
        ly2 = ly + int(ch * 0.17)
        d.rounded_rectangle([lx, ly2, lx + int(lw * 0.7), ly2 + lh], radius=lh // 2, fill=(231, 222, 203, 255))
    # 角丸マスクで再クリップ（ストライプが角丸からはみ出ないように）
    mask = Image.new('L', (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=rad, fill=255)
    if alpha < 255:
        mask = mask.point(lambda a: a * alpha // 255)
    card.putalpha(mask)
    return card.rotate(angle, expand=True, resample=Image.BICUBIC)

def draw_star(img, size, cx, cy, R, r, fill):
    d = ImageDraw.Draw(img)
    Cx = size * cx; Cy = size * cy; RR = size * R; rr = size * r
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = RR if i % 2 == 0 else rr
        pts.append((Cx + rad * math.cos(ang), Cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)

def make_icon(size=512):
    W = H = size
    c0 = (255, 216, 107)  # warm yellow
    c1 = (255, 111, 143)  # pink
    bg = Image.new('RGB', (W, H))
    px = bg.load()
    for y in range(H):
        for x in range(W):
            px[x, y] = lerp(c0, c1, (x + y) / (W + H - 2))
    img = bg.convert('RGBA')

    back = card_layer(size, 9, (255, 255, 255), 95, stripe=False, lines=False)
    img.alpha_composite(back, ((size - back.width) // 2 + int(size * 0.012), (size - back.height) // 2 + int(size * 0.03)))

    front = card_layer(size, -7, (255, 255, 255), 255, stripe=True, lines=True)
    img.alpha_composite(front, ((size - front.width) // 2, (size - front.height) // 2))

    # 星（白い縁取り → 黄色）
    draw_star(img, size, 0.73, 0.26, 0.125, 0.058, (255, 255, 255, 255))
    draw_star(img, size, 0.73, 0.26, 0.105, 0.046, (255, 194, 60, 255))
    return img

ico = make_icon(512)
ico.save('icon-512.png')
ico.resize((192, 192), Image.LANCZOS).save('icon-192.png')
print('icons written:', os.path.abspath('icon-512.png'))
