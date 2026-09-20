import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from core import (DEFAULT_CUSTOM_QUALITY, DEFAULT_CUSTOM_WIDTH, DEFAULT_PRESETS, clone_defaults, create_custom_preset)
assert len(DEFAULT_PRESETS['wordpress'])==4
assert len(DEFAULT_PRESETS['prestashop'])==4
wp=DEFAULT_PRESETS['wordpress']
ps=DEFAULT_PRESETS['prestashop']
assert [(p.width,p.quality,p.mode) for p in wp]==[(800,78,'long_edge'),(1600,80,'long_edge'),(1920,82,'long_edge'),(2560,85,'long_edge')]
assert [(p.width,p.height,p.quality,p.mode) for p in ps]==[(1200,1200,84,'contain'),(2000,2000,85,'contain'),(1920,600,82,'cover'),(1920,800,82,'cover')]
copy=clone_defaults(); copy['wordpress'][0].width=999
assert DEFAULT_PRESETS['wordpress'][0].width==800
print('OK: presets')


class FakeTranslator:
    def text(self, key, **values):
        return {
            'preset_wp_small': 'Petit bloc',
            'preset_ps_square': 'Produit carré',
        }.get(key, key)

assert DEFAULT_PRESETS['wordpress'][0].display_title(FakeTranslator()) == 'Petit bloc'
custom = clone_defaults()['wordpress'][0]
custom.title_custom = True
custom.title = 'Mon preset'
assert custom.display_title(FakeTranslator()) == 'Mon preset'
print('OK: display_title')

custom_preset = create_custom_preset()
assert custom_preset.width == DEFAULT_CUSTOM_WIDTH == 1800
assert custom_preset.quality == DEFAULT_CUSTOM_QUALITY == 82
assert custom_preset.mode == "long_edge" and custom_preset.height is None
assert create_custom_preset(99999, -4).width == 10000
assert create_custom_preset(99999, -4).quality == 1
print("OK: custom export preset")
