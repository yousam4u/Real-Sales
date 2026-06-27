from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math


OUT = Path("assets")
OUT.mkdir(exist_ok=True)


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/Hancom Gothic Bold.ttf" if bold else "C:/Windows/Fonts/Hancom Gothic Regular.ttf",
        "C:/Windows/Fonts/NotoSansKR-VF.ttf",
        "C:/Windows/Fonts/Hancom Gothic Bold.ttf" if bold else "C:/Windows/Fonts/Hancom Gothic Regular.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_centered(draw, text, box, fill, font_obj):
    x1, y1, x2, y2 = box
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    draw.text(
        (x1 + (x2 - x1 - width) / 2, y1 + (y2 - y1 - height) / 2 - 2),
        text,
        fill=fill,
        font=font_obj,
    )


def create_og_image():
    width, height = 1200, 630
    image = Image.new("RGB", (width, height), "#eef7f5")
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            t = (x / width * 0.55) + (y / height * 0.45)
            r = int(238 * (1 - t) + 243 * t)
            g = int(247 * (1 - t) + 223 * t)
            b = int(245 * (1 - t) + 177 * t)
            dx, dy = (x - 890) / 560, (y - 120) / 360
            glow = max(0, 1 - math.sqrt(dx * dx + dy * dy))
            r = min(255, int(r + 24 * glow))
            g = min(255, int(g + 18 * glow))
            b = max(0, int(b - 28 * glow))
            pixels[x, y] = (r, g, b)

    image = image.convert("RGBA")

    wave = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wave)
    draw.polygon(
        [
            (0, 500),
            (120, 454),
            (260, 480),
            (410, 430),
            (590, 350),
            (770, 304),
            (955, 335),
            (1200, 398),
            (1200, 630),
            (0, 630),
        ],
        fill=(18, 62, 68, 45),
    )
    image = Image.alpha_composite(image, wave)

    buildings = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(buildings)
    rects = [(758, 226, 844, 532), (870, 166, 968, 532), (996, 94, 1108, 532), (1136, 186, 1224, 532)]
    for i, rect in enumerate(rects):
        shade = (245, 250, 248, 238) if i % 2 else (226, 237, 235, 232)
        draw.rounded_rectangle(rect, radius=10, fill=shade)
        x1, y1, x2, y2 = rect
        for yy in range(y1 + 34, y2 - 24, 54):
            for xx in range(x1 + 22, x2 - 22, 38):
                draw.rounded_rectangle((xx, yy, xx + 15, yy + 30), radius=2, fill=(18, 62, 68, 38))
    image = Image.alpha_composite(image, buildings.filter(ImageFilter.GaussianBlur(0.2)))

    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    draw.rounded_rectangle((56, 52, 706, 578), radius=38, fill=(6, 23, 28, 85))
    image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(22)))

    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((56, 52, 706, 578), radius=38, fill=(10, 43, 50, 248))
    for gx in range(56, 707, 38):
        draw.line((gx, 52, gx, 578), fill=(255, 255, 255, 18))
    for gy in range(52, 579, 38):
        draw.line((56, gy, 706, gy), fill=(255, 255, 255, 18))

    draw.rounded_rectangle((96, 95, 414, 141), radius=23, fill=(248, 244, 232, 30))
    draw.text((120, 107), "BRAIN CITY MEDIPARK", fill=(248, 244, 232, 235), font=font(18, True))

    draw.text((96, 176), "브레인시티", fill=(255, 255, 255, 255), font=font(74, True))
    draw.text((96, 264), "메디스파크", fill=(255, 255, 255, 255), font=font(74, True))
    draw.text((96, 382), "학교 · 병원 · 공원", fill=(247, 216, 137, 255), font=font(35, True))
    draw.text((96, 426), "미래가치를 가까이 누리는 중심 입지", fill=(247, 216, 137, 255), font=font(35, True))
    draw.text((96, 470), "관심고객 등록 · 타입별 상담 · 방문예약", fill=(220, 232, 231, 255), font=font(23, True))

    chips = [
        ("1,215세대", 96, 514, 156),
        ("84A · 84B · 101", 272, 514, 190),
        ("상담 신청", 482, 514, 182),
    ]
    for text, x, y, chip_width in chips:
        if text == "상담 신청":
            draw.rounded_rectangle((x, y, x + chip_width, y + 48), radius=24, fill=(216, 169, 77, 255))
            fill = (16, 47, 53, 255)
        else:
            draw.rounded_rectangle((x, y, x + chip_width, y + 48), radius=24, fill=(255, 255, 255, 34))
            fill = (255, 255, 255, 255)
        draw_centered(draw, text, (x, y, x + chip_width, y + 48), fill, font(20, True))

    cx, cy = 820, 540
    draw.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), fill=(10, 43, 50, 255))
    draw.polygon(
        [(802, 555), (802, 526), (820, 537), (838, 526), (838, 555), (828, 555), (828, 540), (820, 545), (812, 540), (812, 555)],
        fill=(216, 169, 77, 255),
    )
    draw.rectangle((815, 520, 825, 526), fill=(248, 244, 232, 255))
    draw.rectangle((817, 516, 823, 530), fill=(248, 244, 232, 255))
    draw.text((918, 514), "REAL-SALES", fill=(18, 62, 68, 255), font=font(23, True))
    draw.text((918, 548), "010-6689-2348", fill=(91, 109, 116, 255), font=font(21, True))

    image.convert("RGB").save(OUT / "og-medipark.png", quality=94, optimize=True)


def create_icons():
    size = 512
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    pixels = icon.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)
            pixels[x, y] = (
                int(15 * (1 - t) + 7 * t),
                int(116 * (1 - t) + 27 * t),
                int(125 * (1 - t) + 32 * t),
                255,
            )

    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, size, size), radius=126, fill=255)
    icon.putalpha(mask)

    draw = ImageDraw.Draw(icon)
    draw.polygon(
        [(126, 382), (126, 158), (256, 238), (386, 158), (386, 382), (314, 382), (314, 270), (256, 306), (198, 270), (198, 382)],
        fill=(216, 169, 77, 255),
    )
    draw.rectangle((216, 116, 296, 160), fill=(248, 244, 232, 255))
    draw.rectangle((238, 94, 274, 182), fill=(248, 244, 232, 255))
    draw.line((96, 424, 416, 424), fill=(246, 216, 140, 235), width=18)

    icon.save(OUT / "apple-touch-icon.png")
    icon.resize((32, 32), Image.LANCZOS).save(OUT / "favicon-32.png")


if __name__ == "__main__":
    create_og_image()
    create_icons()
    print("Generated brand assets.")
