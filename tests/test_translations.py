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

custom=json.loads((root/'translations'/'custom.json').read_text(encoding='utf-8'))
assert set(custom)=={file.stem for file in files}
custom_keys=None
for code,values in custom.items():
    assert values and all(isinstance(value,str) and value.strip() for value in values.values()), code
    if custom_keys is None:
        custom_keys=set(values)
    assert set(values)==custom_keys, f"Custom key mismatch: {code}"
assert custom_keys=={
    'custom_title','custom_desc','choose_custom',
    'custom_dimension_title','custom_dimension_desc',
    'custom_quality_title','custom_quality_desc',
    'naming_title','naming_desc','naming_field','naming_example',
}
print(f"OK: Custom translated in {len(custom)} languages")

# Les accolades des libelles du suffixe seraient prises pour des champs de
# formatage par Translator.text(). Seul naming_example a droit a un
# placeholder, et c'est {filename}.
for code,values in custom.items():
    for key in ('naming_title','naming_desc','naming_field'):
        assert '{' not in values[key], f"{code}:{key} ne doit porter aucune accolade"
    placeholders={field for _,field,_,_ in string.Formatter().parse(values['naming_example']) if field}
    assert placeholders=={'filename'}, f"{code}:naming_example -> {placeholders}"
print("OK: no stray braces in naming labels")
