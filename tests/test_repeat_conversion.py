"""Deux lots successifs doivent fonctionner sans redemarrer l'application.

Regression v0.8.5 : le QThread etait detruit par deleteLater a la fin du
premier lot, mais l'attribut Python restait en place. Le garde de
_receive_paths levait alors RuntimeError et le deuxieme depot ne produisait
rien, silencieusement, en version packagee.

Le test ne verifie que le cycle de vie du thread. Les noms de sortie sont
couverts par test_conversion.py.
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

from PIL import Image
from PySide6.QtCore import QEventLoop, QTimer
from PySide6.QtWidgets import QApplication

from app import MainWindow


def pump(milliseconds: int) -> None:
    loop = QEventLoop()
    QTimer.singleShot(milliseconds, loop.quit)
    loop.exec()


def wait_for_idle(window, timeout_ms: int = 30000) -> None:
    elapsed = 0
    while elapsed < timeout_ms:
        pump(100)
        elapsed += 100
        if window.thread is None:
            pump(200)
            return
    raise AssertionError("Le lot ne s'est pas termine dans le temps imparti")


def count_webp(directory: Path) -> int:
    return len(list(directory.glob('*.webp')))


app = QApplication.instance() or QApplication([])

with tempfile.TemporaryDirectory() as raw:
    workspace = Path(raw)
    first = workspace / 'lot-un.jpg'
    second = workspace / 'lot-deux.jpg'
    for path in (first, second):
        Image.new('RGB', (2400, 1600), 'white').save(path, quality=90)

    window = MainWindow()
    window.output_directory = None

    window._receive_paths([str(first)])
    wait_for_idle(window)
    assert count_webp(workspace) == 1, count_webp(workspace)
    assert window.thread is None
    assert window.worker is None

    # Le coeur du test : sans redemarrage, un second depot doit convertir.
    window._receive_paths([str(second)])
    wait_for_idle(window)
    assert count_webp(workspace) == 2, count_webp(workspace)

    # Un troisieme lot, pour verifier que l'etat reste sain dans la duree.
    window._receive_paths([str(first)])
    wait_for_idle(window)
    assert count_webp(workspace) == 3, count_webp(workspace)

    window.close()

print('OK: lots successifs sans redemarrage')
