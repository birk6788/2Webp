from pathlib import Path
text=(Path(__file__).resolve().parents[1]/"app.py").read_text(encoding="utf-8")
assert "QSpinBox" not in text
assert "class NoWheelComboBox" in text
assert "settingsCardsScroll" in text
assert "ScrollBarAlwaysOn" in text
assert "settingsActionBar" in text
assert "resetSettingsButton" in text
assert "saveSettingsButton" in text
assert "QIntValidator" in text
print("OK: safe settings UI")

assert 'language_button=QPushButton("Languages")' in text
assert 'language_combo' not in text
print('OK: Languages menu button')

assert "businessNamesCard" in text
assert "businessNameInput" in text
assert "_collect_business_groups" in text
assert "save_business_groups" in text
assert "choose_usage" in text
print("OK: customizable workflow names")
