import os, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from PIL import Image
from core import Preset, convert_one, unique_webp_destination
with tempfile.TemporaryDirectory() as tmp:
    src=Path(tmp)/'photo.jpg'; Image.new('RGB',(2000,1000),'white').save(src,quality=95)
    dest,before,after=convert_one(src,Preset('test','',False,800,None,80,'long_edge'))
    assert src.exists() and dest.exists() and dest.suffix=='.webp'
    with Image.open(dest) as out: assert out.size==(800,400)
print('OK: conversion')

with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    source=root/'same-name.jpg'
    Image.new('RGB',(300,200),'white').save(source)
    first,_,_=convert_one(source,Preset('test','',False,300,None,80,'long_edge'))
    second,_,_=convert_one(source,Preset('test','',False,300,None,80,'long_edge'))
    assert first.name=='same-name.webp'
    assert second.name=='same-name-2.webp'

with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    source_dir=root/'source'; output_dir=root/'output'
    source_dir.mkdir(); output_dir.mkdir()
    source=source_dir/'photo.jpg'
    Image.new('RGB',(600,400),'white').save(source)
    dest,_,_=convert_one(source,Preset('test','',False,400,None,80,'long_edge'),output_dir)
    assert dest.parent==output_dir
    assert source.exists()
print('OK: safe and custom destinations')
