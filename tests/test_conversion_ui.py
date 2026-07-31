from pathlib import Path

text=(Path(__file__).resolve().parents[1]/"app.py").read_text(encoding="utf-8")

assert "conversionFooter" in text
assert "footerStatus" in text
assert "footerDot" in text
assert "class ElidedLabel" in text
assert "destinationBar" in text
assert "resetDestinationButton" in text
assert "show_result" in text
assert "5000" in text
assert "load_output_directory" in text
assert "save_output_directory" in text
assert "output_dir" in text
assert "QLabel#status" not in text
assert "outputBadge" not in text
assert "status_ready_format" in text
assert "destination_default_value" in text
assert "destination_multiple_origins" in text
assert "_result_destination_text" in text
assert "Modifier la destination" not in text
assert "min(\n            500,\n            max(340, int(self.width() * 0.48))" in text
assert "result_finished.connect(self._update_status)" in text
assert "footer.setFixedHeight(50)" in text
assert "self.setMinimumHeight(258)" in text

print("OK: V0.8.0 conversion layout, destination and temporary result")
