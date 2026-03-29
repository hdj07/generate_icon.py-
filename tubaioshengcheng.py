from PIL import Image, ImageDraw, ImageFont
import os
import random
import time
import argparse


def contrasting_text_color(rgb):
    # simple luminance
    r, g, b = rgb
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return (0, 0, 0, 255) if lum > 160 else (255, 255, 255, 255)


def make_icon(out_path='icon.ico', seed=None):
    if seed is not None:
        random.seed(seed)

    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # random base color
    base = tuple(random.randint(0, 255) for _ in range(3)) + (255,)

    # choose background shape
    shape = random.choice(['circle', 'rounded_rect', 'square'])
    pad = random.randint(8, 24)

    if shape == 'circle':
        draw.ellipse([pad, pad, size - pad, size - pad], fill=base)
    elif shape == 'rounded_rect':
        radius = random.randint(20, 48)
        draw.rounded_rectangle([pad, pad, size - pad, size - pad], radius=radius, fill=base)
    else:
        draw.rectangle([pad, pad, size - pad, size - pad], fill=base)

    # inner white (or slightly tinted) circle
    inner = random.randint(48, 72)
    inner_tint = tuple(min(255, c + random.randint(-10, 10)) for c in (255, 255, 255)) + (255,)
    draw.ellipse([inner, inner, size - inner, size - inner], fill=inner_tint)

    # text: 'AI+' centered
    text = 'AI+'
    font_name = 'arial.ttf'
    font_size = 140
    try:
        font = ImageFont.truetype(font_name, font_size)
    except Exception:
        font = ImageFont.load_default()

    max_width = size - 2 * inner - 20
    # shrink font until fit
    if hasattr(ImageFont, 'FreeTypeFont'):
        while True:
            try:
                bbox = draw.textbbox((0, 0), text, font=font)
                w = bbox[2] - bbox[0]
            except Exception:
                try:
                    w, h = font.getsize(text)
                except Exception:
                    w = max_width
            if w <= max_width or font_size <= 10:
                break
            font_size -= 4
            try:
                font = ImageFont.truetype(font_name, font_size)
            except Exception:
                font = ImageFont.load_default()

    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        try:
            w, h = font.getsize(text)
        except Exception:
            w, h = 100, 100

    text_color = contrasting_text_color(base[:3])
    draw.text(((size - w) / 2, (size - h) / 2 - 8), text, fill=text_color, font=font)

    # small accent (optional)
    if random.random() < 0.4:
        accent_color = tuple(random.randint(0, 255) for _ in range(3)) + (180,)
        ax = random.randint(size - 60, size - 20)
        ay = random.randint(20, 60)
        draw.ellipse([ax - 8, ay - 8, ax + 8, ay + 8], fill=accent_color)

    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(out_path, format='ICO', sizes=sizes)


def random_filename():
    return f"icon_{int(time.time())}_{random.getrandbits(32):08x}.ico"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', '-n', type=int, default=1, help='generate N random icons')
    parser.add_argument('--seed', type=int, default=None, help='optional random seed')
    args = parser.parse_args()

    outs = []
    for i in range(args.count):
        name = random_filename()
        out = os.path.join(os.getcwd(), name)
        make_icon(out, seed=(args.seed or None))
        outs.append(out)
        print('Wrote', out)