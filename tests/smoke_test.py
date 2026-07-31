import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from app import MainWindow
app=QApplication.instance() or QApplication([])
window=MainWindow()
assert window.windowTitle()=='2Webp'
assert window.pages.count()==2
assert len(window.language_menu.actions())==22
assert window.language_button.text()=='Languages'
assert window.language_menu.actions()[0].text()=='Français'
assert not bool(window.windowFlags() & Qt.WindowType.WindowMaximizeButtonHint)
assert len(window.editor_cards['wordpress'])==4 and len(window.editor_cards['prestashop'])==4
assert window.drop_zone.destination_button is not None
assert window.drop_zone.reset_destination_button is not None
assert window.status.objectName()=='footerStatus'
assert not hasattr(window, 'output_badge')
window.close()
print('OK: GUI smoke test')
assert 'WebP' in window.status.toolTip()
