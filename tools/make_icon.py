"""Draw the app icon (a 1-bit radar scope in the classic Mac style) and write it for
every platform: platform/icon.png, platform/windows/atc.ico, platform/macos/atc.icns.

    python tools/make_icon.py
"""
import math, os
from PIL import Image, ImageDraw

N = 64                                   # drawn on a 64x64 pixel grid, scaled up crisp
img = Image.new('RGBA', (N, N), (0, 0, 0, 0))
px = img.load()
BLACK, WHITE, GRAY = (0, 0, 0, 255), (255, 255, 255, 255), (60, 60, 60, 255)

# rounded square backdrop
d = ImageDraw.Draw(img)
d.rounded_rectangle([1, 1, N - 2, N - 2], radius=10, fill=GRAY)

cx = cy = (N - 1) / 2
R = 26
for y in range(N):
    for x in range(N):
        r = math.hypot(x - cx, y - cy)
        if r <= R - 2.5:
            px[x, y] = WHITE
        elif r <= R:
            px[x, y] = BLACK
# dot grid and dashed sector lines, as on the game's radar
for y in range(N):
    for x in range(N):
        if math.hypot(x - cx, y - cy) > R - 4:
            continue
        if (x % 8 == 3) and (y % 8 == 3):
            px[x, y] = BLACK
for ang in range(0, 360, 45):
    a = math.radians(ang)
    for t in range(0, R - 2):
        if t > 2 and (t % 6) < 4:
            x, y = round(cx + t * math.cos(a)), round(cy + t * math.sin(a))
            px[x, y] = BLACK
# sweep line
a = math.radians(-55)
for t in range(0, R - 2):
    px[round(cx + t * math.cos(a)), round(cy + t * math.sin(a))] = BLACK
# a jet blip with its number box
for x, y in [(20, 22), (21, 22), (22, 22), (19, 23), (20, 23), (21, 23), (22, 23), (23, 23), (20, 24), (21, 24), (22, 24)]:
    px[x, y] = BLACK
d.rectangle([38, 36, 44, 42], fill=BLACK)
for x, y in [(40, 38), (41, 38), (41, 39), (40, 40), (41, 40), (40, 41), (41, 41)]:
    px[x, y] = WHITE

root = os.path.join(os.path.dirname(__file__), '..', 'platform')
os.makedirs(os.path.join(root, 'windows'), exist_ok=True)
os.makedirs(os.path.join(root, 'macos'), exist_ok=True)
big = img.resize((1024, 1024), Image.NEAREST)
big.save(os.path.join(root, 'icon.png'))
img.resize((256, 256), Image.NEAREST).save(os.path.join(root, 'windows', 'atc.ico'),
                                          sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
big.save(os.path.join(root, 'macos', 'atc.icns'))
print('icons written to', os.path.abspath(root))
