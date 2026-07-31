from pathlib import Path
root=Path(__file__).resolve().parents[1]
for file in root.rglob('*'):
    if file.is_file() and file.suffix.lower() in {'.py','.ps1','.md','.txt','.json'}:
        text=file.read_text(encoding='utf-8',errors='ignore').lower()
        legacy='to'+' webp'
        legacy_file='to'+'-webp'
        assert legacy not in text, f"Legacy brand in {file}"
        assert legacy_file not in text, f"Legacy filename in {file}"
print('OK: clean 2Webp branding')
