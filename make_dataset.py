from PIL import Image, ImageFont, ImageDraw
from tqdm import tqdm
import os

# https://ja.wikipedia.org/wiki/Shift_JIS#%E5%8C%BA%E7%82%B9%E7%95%AA%E5%8F%B7%E3%81%8B%E3%82%89%E3%81%AE%E5%A4%89%E6%8F%9B


def s1(k, t):
    if 1 <= k <= 62:
        return (k+257)//2
    if 63 <= k <= 94:
        return (k+385)//2


def s2(k, t):
    if k % 2 == 1:
        if 1 <= t <= 63:
            return t+63
        if 64 <= t <= 94:
            return t+64
    else:
        return t+158


def get_chars():
    chars = []

    for b in list(range(0x20, 0x7f))+list(range(0xa1, 0xdf+1)):
        s = bytearray([b]).decode('cp932')
        chars.append((b, s))

    for k in range(1, 94+1):
        for t in range(1, 94+1):
            try:
                ba = bytearray([s1(k, t), s2(k, t)])
                s = ba.decode('cp932')
                chars.append((ba[0]*0x100+ba[1], s))
            except UnicodeDecodeError:
                pass

    return chars


def main():
    chars = get_chars()

    for FONT in ('meiryo', 'msmincho', 'msgothic'):
        font_file = r"C:\Windows\Fonts\%s.ttc" % FONT

        if FONT == 'meiryo':
            font_size = 32
        elif FONT == 'msmincho':
            font_size = 30
        elif FONT == 'msgothic':
            font_size = 30
        font = ImageFont.truetype(font=font_file, size=font_size)

        if FONT == 'meiryo':
            xy = (-2, -8)
        elif FONT == 'msmincho':
            xy = (-1, -1)
        elif FONT == 'msgothic':
            xy = (-1, -1)
        else:
            assert False

        for i, s in tqdm(chars):
            try:
                im = Image.new(mode='L', size=(28, 28), color=0)
                draw = ImageDraw.Draw(im)
                draw.text(xy=xy, text=s, font=font, fill=255)
                os.makedirs('dataset/cp932_hex/%d' % i, exist_ok=True)
                im.save('dataset/cp932_hex/%d/%s.png' % (i, FONT))
            except UnicodeDecodeError:
                pass


if __name__ == '__main__':
    main()
