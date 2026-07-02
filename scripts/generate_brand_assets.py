from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
HERO = ROOT / "hero_render" / "hero_render.jpg"
OUT.mkdir(exist_ok=True)

BRAND = (14, 79, 71, 255)
BRAND_DARK = (8, 47, 42, 255)
INK = (23, 31, 29, 255)
GOLD = (185, 151, 91, 255)
GOLD_LIGHT = (233, 220, 192, 255)
CREAM = (247, 244, 236, 255)
WHITE = (255, 255, 255, 255)


def font(size: int, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if serif:
        candidates.extend([
            r"C:\Windows\Fonts\batang.ttc",
            r"C:\Windows\Fonts\malgun.ttf",
        ])
    elif bold:
        candidates.extend([
            r"C:\Windows\Fonts\malgunbd.ttf",
            r"C:\Windows\Fonts\malgun.ttf",
        ])
    else:
        candidates.extend([
            r"C:\Windows\Fonts\malgun.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ])

    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def cover_image(path: Path, size: tuple[int, int], focus_y: float = 0.42) -> Image.Image:
    image = Image.open(path).convert("RGB")
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)
    left = (resized.width - target_w) // 2
    max_top = max(0, resized.height - target_h)
    top = round(max_top * focus_y)
    return resized.crop((left, top, left + target_w, top + target_h))


def rounded_rect(draw: ImageDraw.ImageDraw, xy, radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def text(draw: ImageDraw.ImageDraw, xy, value: str, fill, font_obj, anchor=None) -> None:
    draw.text(xy, value, fill=fill, font=font_obj, anchor=anchor)


def make_gradient(size: tuple[int, int]) -> Image.Image:
    w, h = size
    gradient = Image.new("RGBA", size)
    pixels = gradient.load()
    for y in range(h):
        for x in range(w):
            t = (x / w * 0.55) + (y / h * 0.45)
            r = round(BRAND_DARK[0] * (1 - t) + BRAND[0] * t)
            g = round(BRAND_DARK[1] * (1 - t) + BRAND[1] * t)
            b = round(BRAND_DARK[2] * (1 - t) + BRAND[2] * t)
            pixels[x, y] = (r, g, b, 232)
    return gradient


def create_og_canvas() -> Image.Image:
    canvas = Image.new("RGBA", (1200, 630), CREAM)
    draw = ImageDraw.Draw(canvas)

    if HERO.exists():
        hero = cover_image(HERO, (1200, 630), focus_y=0.2).convert("RGBA")
        hero = hero.filter(ImageFilter.GaussianBlur(0.35))
        canvas.alpha_composite(hero)

    canvas.alpha_composite(make_gradient((1200, 630)))
    draw.rectangle((0, 0, 1200, 630), fill=(8, 47, 42, 88))

    # Subtle gold framing and premium corner mark.
    draw.line((54, 54, 1146, 54), fill=(233, 220, 192, 180), width=2)
    draw.line((54, 576, 1146, 576), fill=(233, 220, 192, 120), width=2)
    draw.line((54, 54, 54, 576), fill=(233, 220, 192, 110), width=2)
    draw.line((1146, 54, 1146, 576), fill=(233, 220, 192, 110), width=2)
    draw.rectangle((54, 54, 250, 60), fill=GOLD)
    draw.rectangle((950, 570, 1146, 576), fill=GOLD)

    rounded_rect(draw, (76, 82, 446, 128), 23, fill=(255, 255, 255, 42), outline=(233, 220, 192, 130), width=1)
    text(draw, (100, 94), "PYEONGTAEK BRAINCITY 6BL", GOLD_LIGHT, font(22, bold=True))

    text(draw, (84, 182), "브레인시티", WHITE, font(78, bold=True, serif=True))
    text(draw, (84, 274), "메디스파크", WHITE, font(90, bold=True, serif=True))
    text(draw, (88, 368), "로제비앙 모아엘가", GOLD_LIGHT, font(54, bold=True, serif=True))

    text(draw, (88, 454), "학교·병원·상권, 전부 걸어서 닿는 자리", WHITE, font(34, bold=True))
    text(draw, (90, 504), "59형 분양 마감 · 84A / 84B / 101 타입 상담 가능", GOLD_LIGHT, font(27, bold=True))

    # Right-side compact info panel.
    panel = Image.new("RGBA", (330, 382), (255, 255, 255, 235))
    panel_draw = ImageDraw.Draw(panel)
    rounded_rect(panel_draw, (0, 0, 330, 382), 26, fill=(255, 255, 255, 235), outline=(233, 220, 192, 255), width=2)
    panel_draw.rectangle((0, 0, 330, 9), fill=GOLD)
    text(panel_draw, (34, 48), "사전등록", BRAND_DARK, font(28, bold=True))
    text(panel_draw, (34, 88), "우선 안내", BRAND_DARK, font(46, bold=True, serif=True))
    panel_draw.line((34, 150, 296, 150), fill=GOLD_LIGHT, width=2)
    for i, item in enumerate(["도보 통학권", "아주대병원 예정", "중심상업지역 인접"]):
        y = 188 + i * 52
        panel_draw.ellipse((34, y, 50, y + 16), fill=GOLD)
        text(panel_draw, (66, y - 4), item, INK, font(25, bold=True))
    text(panel_draw, (34, 340), "010-6689-2348", BRAND, font(30, bold=True))
    canvas.alpha_composite(panel, (790, 124))

    return canvas.convert("RGB")


def create_og_image() -> None:
    image = create_og_canvas()
    image.save(OUT / "og-medipark-premium.png", quality=95, optimize=True)
    image.save(OUT / "og-medipark.png", quality=95, optimize=True)


def create_icon_canvas(size: int) -> Image.Image:
    scale = size / 512
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)

    def p(value: int) -> int:
        return round(value * scale)

    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((p(54), p(54), p(458), p(458)), radius=p(112), fill=(0, 0, 0, 95))
    icon.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(p(18))))

    draw.rounded_rectangle((p(54), p(48), p(458), p(452)), radius=p(112), fill=BRAND_DARK)
    draw.rounded_rectangle((p(76), p(70), p(436), p(430)), radius=p(94), outline=GOLD, width=max(2, p(14)))

    # Apartment tower + medical cross mark, kept simple for 16px legibility.
    draw.rounded_rectangle((p(160), p(172), p(232), p(340)), radius=p(18), fill=WHITE)
    draw.rounded_rectangle((p(280), p(172), p(352), p(340)), radius=p(18), fill=WHITE)
    draw.rectangle((p(184), p(202), p(208), p(230)), fill=BRAND)
    draw.rectangle((p(304), p(202), p(328), p(230)), fill=BRAND)
    draw.rectangle((p(184), p(258), p(208), p(286)), fill=BRAND)
    draw.rectangle((p(304), p(258), p(328), p(286)), fill=BRAND)

    draw.rounded_rectangle((p(226), p(356), p(286), p(390)), radius=p(12), fill=GOLD)
    draw.polygon([(p(132), p(176)), (p(256), p(98)), (p(380), p(176)), (p(352), p(208)), (p(256), p(148)), (p(160), p(208))], fill=GOLD)

    draw.rounded_rectangle((p(238), p(206), p(274), p(286)), radius=p(9), fill=GOLD_LIGHT)
    draw.rounded_rectangle((p(216), p(228), p(296), p(264)), radius=p(9), fill=GOLD_LIGHT)
    draw.line((p(140), p(404), p(372), p(404)), fill=GOLD_LIGHT, width=max(2, p(15)))
    return icon


def create_icons() -> None:
    icon_512 = create_icon_canvas(512)
    icon_512.save(OUT / "apple-touch-icon.png")
    icon_32 = icon_512.resize((32, 32), Image.LANCZOS)
    icon_32.save(OUT / "favicon-premium-32.png")
    icon_32.save(OUT / "favicon-32.png")
    icon_512.save(OUT / "favicon-premium.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    icon_512.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

    svg = """<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 512 512\"><rect x=\"54\" y=\"48\" width=\"404\" height=\"404\" rx=\"112\" fill=\"#082F2A\"/><rect x=\"76\" y=\"70\" width=\"360\" height=\"360\" rx=\"94\" fill=\"none\" stroke=\"#B9975B\" stroke-width=\"14\"/><path d=\"M132 176 256 98l124 78-28 32-96-60-96 60z\" fill=\"#B9975B\"/><rect x=\"160\" y=\"172\" width=\"72\" height=\"168\" rx=\"18\" fill=\"#fff\"/><rect x=\"280\" y=\"172\" width=\"72\" height=\"168\" rx=\"18\" fill=\"#fff\"/><rect x=\"238\" y=\"206\" width=\"36\" height=\"80\" rx=\"9\" fill=\"#E9DCC0\"/><rect x=\"216\" y=\"228\" width=\"80\" height=\"36\" rx=\"9\" fill=\"#E9DCC0\"/><rect x=\"226\" y=\"356\" width=\"60\" height=\"34\" rx=\"12\" fill=\"#B9975B\"/><path d=\"M140 404h232\" stroke=\"#E9DCC0\" stroke-width=\"15\" stroke-linecap=\"round\"/></svg>"""
    (OUT / "favicon-premium.svg").write_text(svg, encoding="utf-8")
    (OUT / "favicon.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    create_og_image()
    create_icons()
    print("Generated refreshed favicon and OG thumbnail assets.")