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
    assert dest.name=='photo_800.webp'
    with Image.open(dest) as out: assert out.size==(800,400)
print('OK: conversion')

with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    source=root/'same-name.jpg'
    Image.new('RGB',(300,200),'white').save(source)
    first,_,_=convert_one(source,Preset('test','',False,300,None,80,'long_edge'))
    second,_,_=convert_one(source,Preset('test','',False,300,None,80,'long_edge'))
    assert first.name=='same-name_300.webp'
    assert second.name=='same-name_300-2.webp'

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

# Le suffixe porte le bord long reellement produit, pas la valeur du preset.
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)

    # Bord long : une source plus petite que le preset n'est jamais agrandie.
    petite=root/'petite.jpg'
    Image.new('RGB',(1200,800),'white').save(petite)
    dest,_,_=convert_one(petite,Preset('test','',False,1600,None,80,'long_edge'))
    assert dest.name=='petite_1200.webp', dest.name

    # Portrait : le bord long est la hauteur.
    portrait=root/'portrait.jpg'
    Image.new('RGB',(1000,2500),'white').save(portrait)
    dest,_,_=convert_one(portrait,Preset('test','',False,1600,None,80,'long_edge'))
    assert dest.name=='portrait_1600.webp', dest.name

    # Adapter au cadre : le canevas fixe donne toujours le meme bord long.
    carre=root/'carre.jpg'
    Image.new('RGB',(3000,2000),'white').save(carre)
    dest,_,_=convert_one(carre,Preset('test','',False,1200,1200,84,'contain'))
    assert dest.name=='carre_1200.webp', dest.name

    # Recadrer pour remplir : idem, bord long du format cible.
    banniere=root/'banniere.jpg'
    Image.new('RGB',(4000,3000),'white').save(banniere)
    dest,_,_=convert_one(banniere,Preset('test','',False,1920,600,82,'cover'))
    assert dest.name=='banniere_1920.webp', dest.name

    # Deux tailles differentes de la meme source ne se disputent plus le nom.
    source=root/'serie.jpg'
    Image.new('RGB',(3000,2000),'white').save(source)
    petit,_,_=convert_one(source,Preset('test','',False,800,None,78,'long_edge'))
    grand,_,_=convert_one(source,Preset('test','',False,1920,None,82,'long_edge'))
    assert petit.name=='serie_800.webp', petit.name
    assert grand.name=='serie_1920.webp', grand.name

# Sans bord long fourni, le nom reste celui de la source.
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    source=root/'brut.jpg'
    Image.new('RGB',(400,400),'white').save(source)
    assert unique_webp_destination(source).name=='brut.webp'
    assert unique_webp_destination(source,None,"_1600").name=='brut_1600.webp'

print('OK: suffixe de bord long dans le nom de sortie')

# Suffixe libre choisi dans les Reglages.
from core import DEFAULT_NAME_SUFFIX, render_name_suffix, sanitize_name_suffix

assert DEFAULT_NAME_SUFFIX == "_{long}"

# Les balises anglaises et leurs alias francais donnent le meme resultat.
assert render_name_suffix("_{long}", 1600, 1200, 82) == "_1600"
assert render_name_suffix("_{bordlong}", 1600, 1200, 82) == "_1600"
assert render_name_suffix("_{width}x{height}", 1600, 1200, 82) == "_1600x1200"
assert render_name_suffix("_{largeur}x{hauteur}", 1600, 1200, 82) == "_1600x1200"
assert render_name_suffix("_{long}_q{quality}", 1600, 1200, 82) == "_1600_q82"

# Le bord long suit l'orientation reelle.
assert render_name_suffix("_{long}", 1000, 2500, 80) == "_2500"

# Un suffixe libre sans balise passe tel quel.
assert render_name_suffix("-web", 1600, 1200, 82) == "-web"

# Une balise inconnue reste visible : l'utilisateur la corrige.
assert render_name_suffix("_{inconnu}", 1600, 1200, 82) == "_{inconnu}"

# Les caracteres interdits par Windows sont retires.
for interdit in '\\/:*?"<>|':
    assert interdit not in sanitize_name_suffix("a" + interdit + "b")
assert sanitize_name_suffix("  _web  ") == "_web"
assert sanitize_name_suffix("_web.") == "_web"

with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    source=root/'photo.jpg'
    Image.new('RGB',(3000,2000),'white').save(source)
    preset=Preset('test','',False,1600,None,82,'long_edge')

    # Suffixe vide : le nom d'origine est conserve, comme avant la 0.8.6.
    dest,_,_=convert_one(source,preset,None,"")
    assert dest.name=='photo.webp', dest.name

    # Suffixe libre.
    dest,_,_=convert_one(source,preset,None,"-web")
    assert dest.name=='photo-web.webp', dest.name

    # Suffixe avec balises.
    dest,_,_=convert_one(source,preset,None,"_{width}x{height}_q{quality}")
    assert dest.name=='photo_1600x1067_q82.webp', dest.name

    # La protection contre l'ecrasement passe avant le suffixe choisi.
    encore,_,_=convert_one(source,preset,None,"-web")
    assert encore.name=='photo-web-2.webp', encore.name

print('OK: suffixe de nom libre et balises')
