from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OG_SOURCE = OUT / "og-medipark-source.png"

OUT.mkdir(exist_ok=True)

DEEP_NAVY = (5, 18, 32, 255)
NAVY = (10, 42, 64, 255)
GOLD = (210, 162, 73, 255)
LIGHT_GOLD = (247, 218, 151, 255)
WHITE = (255, 255, 255, 255)


def cover_image(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def create_og_image() -> None:
    if not OG_SOURCE.exists():
        raise FileNotFoundError(f"Missing OG source image: {OG_SOURCE}")

    image = cover_image(OG_SOURCE, (1200, 630)).convert("RGB")
    image.save(OUT / "og-medipark.png", quality=94, optimize=True)


def create_icon_canvas(size: int) -> Image.Image:
    scale = size / 512
    icon = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    def p(value: int) -> int:
        return round(value * scale)

    # Soft high-contrast shadow keeps the transparent favicon readable on light tabs.
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.polygon(
        [
            (p(84), p(392)),
            (p(84), p(196)),
            (p(162), p(148)),
            (p(256), p(86)),
            (p(350), p(148)),
            (p(428), p(196)),
            (p(428), p(392)),
        ],
        fill=(0, 0, 0, 100),
    )
    icon.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(p(18))))

    # Deep navy architectural body.
    draw.polygon(
        [
            (p(84), p(392)),
            (p(84), p(196)),
            (p(162), p(148)),
            (p(256), p(86)),
            (p(350), p(148)),
            (p(428), p(196)),
            (p(428), p(392)),
        ],
        fill=DEEP_NAVY,
    )

    # Gold premium roofline / entrance axis.
    draw.polygon(
        [(p(100), p(196)), (p(256), p(96)), (p(412), p(196)), (p(372), p(226)), (p(256), p(152)), (p(140), p(226))],
        fill=GOLD,
    )
    draw.rectangle((p(224), p(230), p(288), p(392)), fill=GOLD)

    # Minimal skyline windows, intentionally large enough for 16px rendering.
    for x in (p(132), p(172), p(340), p(380)):
        draw.rounded_rectangle((x, p(248), x + p(22), p(326)), radius=p(5), fill=WHITE)
    draw.rounded_rectangle((p(230), p(176), p(282), p(212)), radius=p(6), fill=WHITE)

    # Ground line gives the mark stability without adding text.
    draw.line((p(76), p(424), p(436), p(424)), fill=LIGHT_GOLD, width=max(1, p(18)))

    icon.alpha_composite(layer)
    return icon


def create_icons() -> None:
    icon_512 = create_icon_canvas(512)
    icon_512.save(OUT / "apple-touch-icon.png")
    icon_512.resize((32, 32), Image.LANCZOS).save(OUT / "favicon-32.png")
    icon_512.save(
        OUT / "favicon.ico",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )


if __name__ == "__main__":
    create_og_image()
    create_icons()
    print("Generated premium favicon and OG thumbnail assets.")
