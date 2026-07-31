import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core import DEFAULT_BUSINESS_GROUPS, clone_default_business_groups


class FakeTranslator:
    def text(self, key, **values):
        return {
            "wp_title": "WordPress / Web",
            "ps_title": "PrestaShop",
        }.get(key, key)


translator = FakeTranslator()

assert DEFAULT_BUSINESS_GROUPS["wordpress"].display_title(translator) == "WordPress / Web"
assert DEFAULT_BUSINESS_GROUPS["prestashop"].display_title(translator) == "PrestaShop"

groups = clone_default_business_groups()
groups["prestashop"].title = "Shopify"
groups["prestashop"].title_custom = True

assert groups["prestashop"].display_title(translator) == "Shopify"
assert DEFAULT_BUSINESS_GROUPS["prestashop"].display_title(translator) == "PrestaShop"

print("OK: customizable business groups")
