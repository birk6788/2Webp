from pathlib import Path
import json, string
root=Path(__file__).resolve().parents[1]
files=sorted((root/'translations').glob('??.json'))
assert len(files)==22, f"22 languages expected, got {len(files)}"
reference=None
for file in files:
    data=json.loads(file.read_text(encoding='utf-8'))
    assert data and all(isinstance(v,str) and v.strip() for v in data.values()), file.name
    if reference is None:
        reference=set(data)
        ref_data=data
    assert set(data)==reference, f"Key mismatch: {file.name}"
    for key,value in data.items():
        placeholders={field for _,field,_,_ in string.Formatter().parse(value) if field}
        ref_placeholders={field for _,field,_,_ in string.Formatter().parse(ref_data[key]) if field}
        assert placeholders==ref_placeholders, f"Placeholder mismatch {file.name}:{key}"
print(f"OK: {len(files)} translations, {len(reference)} keys")
