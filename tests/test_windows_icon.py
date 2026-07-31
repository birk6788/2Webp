from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
BUILD = (ROOT / "build.ps1").read_text(encoding="utf-8")

assert "SetCurrentProcessExplicitAppUserModelID" in APP
assert "fr.jpbloch.2webp" in APP
assert "app.setWindowIcon" in APP
assert "2Webp-taskbar-round.ico" in APP
assert "2Webp-taskbar-round.png" in APP
assert "2Webp-taskbar-round.ico" in BUILD

png_path = ROOT / "assets" / "brand" / "2Webp-taskbar-round.png"
ico_path = ROOT / "assets" / "brand" / "2Webp-taskbar-round.ico"
assert png_path.exists() and ico_path.exists()

png = Image.open(png_path).convert("RGBA")
bbox = png.getchannel("A").getbbox()
assert bbox is not None
assert 8 <= bbox[0] <= 20 and 236 <= bbox[2] <= 248, bbox

ico = Image.open(ico_path)
sizes = ico.info.get("sizes", set())
for expected in {(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)}:
    assert expected in sizes, (expected, sizes)

print("OK: balanced multiresolution Windows icon")
