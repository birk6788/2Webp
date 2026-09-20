from pathlib import Path

text = (Path(__file__).resolve().parents[1] / "app.py").read_text(encoding="utf-8")

assert "self.setFixedHeight(124)" in text
assert "presetMode" in text
assert "font-size:25px" in text
assert "font-size:12px" in text
assert "indicator:unchecked" in text and "background:#F4F6FA" in text
assert "indicator:checked" in text and "background:#FF6B2C" in text
assert "layout.addSpacing(3)" in text
assert "layout.addSpacing(18)" in text

print("OK: preserved preset height and strengthened hierarchy")

assert 'ModeCard("custom")' in text
assert "class CustomFieldCard" in text
assert "custom_width_card" in text and "custom_quality_card" in text
assert 'QLineEdit#customValueInput' in text
assert 'self.custom_widget.setVisible(mode=="custom")' in text
print("OK: direct Custom mode with long edge and WebP quality")

assert 'self.preset.key.startswith("ps-")' in text
assert 'self.mode_label.setSizePolicy' in text
assert 'self.preset_grid.setColumnStretch(index, 1)' in text
print("OK: PrestaShop cards cannot force horizontal overflow")
