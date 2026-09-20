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

assert "load_custom_export" in text and "save_custom_export" in text
assert "DEFAULT_CUSTOM_WIDTH" in text and "DEFAULT_CUSTOM_QUALITY" in text
print("OK: persisted Custom values and default reset")

assert "class NameSuffixCard" in text
assert "load_name_suffix" in text and "save_name_suffix" in text
assert "_collect_name_suffix" in text
assert "namingTags" in text and "namingExample" in text
assert "refresh_example" in text
# Le suffixe doit suivre le lot jusqu'au thread de conversion.
assert "self.name_suffix," in text
print("OK: editable output name suffix")
