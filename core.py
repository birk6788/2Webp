from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageOps

SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


GROUP_TITLE_KEYS = {
    "wordpress": "wp_title",
    "prestashop": "ps_title",
}


PRESET_TITLE_KEYS = {
    "wp-1": "preset_wp_small",
    "wp-2": "preset_wp_web",
    "wp-3": "preset_wp_silo",
    "wp-4": "preset_wp_gallery",
    "ps-1": "preset_ps_square",
    "ps-2": "preset_ps_square_hd",
    "ps-3": "preset_ps_category",
    "ps-4": "preset_ps_home",
}


@dataclass
class BusinessGroup:
    key: str
    title: str
    title_custom: bool

    def display_title(self, translator) -> str:
        """Return the custom workflow name or its translated default."""
        if self.title_custom and self.title.strip():
            return self.title.strip()

        translation_key = GROUP_TITLE_KEYS.get(self.key)
        if translation_key is None:
            return self.title.strip() or self.key

        return translator.text(translation_key)


DEFAULT_BUSINESS_GROUPS = {
    "wordpress": BusinessGroup("wordpress", "", False),
    "prestashop": BusinessGroup("prestashop", "", False),
}


def clone_default_business_groups() -> dict[str, BusinessGroup]:
    return {
        key: BusinessGroup(**asdict(group))
        for key, group in DEFAULT_BUSINESS_GROUPS.items()
    }


@dataclass
class Preset:
    key: str
    title: str
    title_custom: bool
    width: int
    height: int | None
    quality: int
    mode: str

    def display_title(self, translator) -> str:
        """Return the custom title or the translated default title."""
        if self.title_custom and self.title.strip():
            return self.title.strip()

        translation_key = PRESET_TITLE_KEYS.get(self.key)
        if translation_key is None:
            return self.title.strip() or self.key

        return translator.text(translation_key)


DEFAULT_PRESETS = {
    'wordpress': [
        Preset('wp-1', '', False, 800, None, 78, 'long_edge'),
        Preset('wp-2', '', False, 1600, None, 80, 'long_edge'),
        Preset('wp-3', '', False, 1920, None, 82, 'long_edge'),
        Preset('wp-4', '', False, 2560, None, 85, 'long_edge'),
    ],
    'prestashop': [
        Preset('ps-1', '', False, 1200, 1200, 84, 'contain'),
        Preset('ps-2', '', False, 2000, 2000, 85, 'contain'),
        Preset('ps-3', '', False, 1920, 600, 82, 'cover'),
        Preset('ps-4', '', False, 1920, 800, 82, 'cover'),
    ],
}


def clone_defaults() -> dict[str, list[Preset]]:
    return {
        group: [Preset(**asdict(item)) for item in items]
        for group, items in DEFAULT_PRESETS.items()
    }


def iter_image_files(paths: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)
        elif path.is_dir():
            files.extend(
                item
                for item in sorted(path.iterdir())
                if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS
            )

    unique: list[Path] = []
    seen: set[Path] = set()
    for path in files:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def resize_long_edge(image: Image.Image, long_edge: int) -> Image.Image:
    width, height = image.size
    current = max(width, height)
    if current <= long_edge:
        return image.copy()
    ratio = long_edge / current
    size = (max(1, round(width * ratio)), max(1, round(height * ratio)))
    return image.resize(size, Image.Resampling.LANCZOS)


def contain_on_canvas(image: Image.Image, width: int, height: int) -> Image.Image:
    fitted = ImageOps.contain(image, (width, height), Image.Resampling.LANCZOS)
    left = (width - fitted.width) // 2
    top = (height - fitted.height) // 2

    if 'A' in fitted.getbands():
        canvas = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        canvas.alpha_composite(fitted.convert('RGBA'), (left, top))
    else:
        canvas = Image.new('RGB', (width, height), 'white')
        canvas.paste(fitted.convert('RGB'), (left, top))
    return canvas


def cover_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    return ImageOps.fit(
        image,
        (width, height),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )


def unique_webp_destination(source: Path, output_dir: Path | None = None) -> Path:
    """Return a non-existing WebP path without overwriting an earlier file."""
    directory = Path(output_dir) if output_dir is not None else source.parent
    if not directory.is_dir():
        raise FileNotFoundError(f'Output directory is unavailable: {directory}')

    candidate = directory / f"{source.stem}.webp"
    suffix = 2
    while candidate.exists():
        candidate = directory / f"{source.stem}-{suffix}.webp"
        suffix += 1
    return candidate


def convert_one(
    source: Path,
    preset: Preset,
    output_dir: Path | None = None,
) -> tuple[Path, int, int]:
    destination = unique_webp_destination(source, output_dir)
    before = source.stat().st_size

    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened)
        icc_profile = image.info.get('icc_profile')

        if preset.mode == 'long_edge':
            output = resize_long_edge(image, preset.width)
        elif preset.mode == 'contain':
            if preset.height is None:
                raise ValueError('Missing height')
            output = contain_on_canvas(image, preset.width, preset.height)
        elif preset.mode == 'cover':
            if preset.height is None:
                raise ValueError('Missing height')
            output = cover_crop(image, preset.width, preset.height)
        else:
            raise ValueError(f'Unknown mode: {preset.mode}')

        output = output.convert('RGBA' if 'A' in output.getbands() else 'RGB')
        options = {'format': 'WEBP', 'quality': preset.quality, 'method': 6}
        if icc_profile:
            options['icc_profile'] = icc_profile
        output.save(destination, **options)

    return destination, before, destination.stat().st_size
