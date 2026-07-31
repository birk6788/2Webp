from __future__ import annotations

import json
import sys
import ctypes
from dataclasses import asdict
from pathlib import Path

from PySide6.QtCore import QEvent, QObject, QStandardPaths, QThread, Qt, Signal, QTimer
from PySide6.QtGui import QIcon, QIntValidator, QPixmap
from core import (
    BusinessGroup, GROUP_TITLE_KEYS, PRESET_TITLE_KEYS, Preset, clone_default_business_groups,
    clone_defaults, convert_one, iter_image_files,
)

from PySide6.QtWidgets import (
    QApplication, QButtonGroup, QComboBox, QFileDialog, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QProgressBar, QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QStackedWidget, QVBoxLayout, QWidget,
)

APP_NAME = "2Webp"
APP_VERSION = "0.8.0"


def app_icon_path() -> Path:
    """Icône ronde utilisée par Qt, Windows et l’exécutable."""
    filename = (
        "2Webp-taskbar-round.ico"
        if sys.platform == "win32"
        else "2Webp-taskbar-round.png"
    )
    return resource_dir() / "assets" / "brand" / filename


def configure_windows_app_identity() -> None:
    """Empêche Windows de regrouper 2Webp sous l’icône générique de Python."""
    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "fr.jpbloch.2webp"
        )
    except Exception:
        # L’application reste fonctionnelle sur les versions de Windows atypiques.
        pass
LEGACY_DEFAULT_TITLES = {
    "wp-1": {"Petit bloc"}, "wp-2": {"Web / devis"},
    "wp-3": {"Page silo"}, "wp-4": {"Galerie HD"},
    "ps-1": {"Produit carré"}, "ps-2": {"Produit carré HD"},
    "ps-3": {"Bannière catégorie"}, "ps-4": {"Bannière accueil"},
}


def resource_dir() -> Path:
    return Path(__file__).resolve().parent


def app_data_dir() -> Path:
    base = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
    path = Path(base) / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def presets_path() -> Path:
    return app_data_dir() / "presets.json"


def settings_path() -> Path:
    return app_data_dir() / "settings.json"


class Translator:
    def __init__(self, language: str):
        self.names = json.loads((resource_dir()/"translations"/"languages.json").read_text(encoding="utf-8"))
        self.fallback = self._load("fr")
        self.language = language if language in self.names else "fr"
        self.data = self._load(self.language)

    def _load(self, code: str) -> dict[str, str]:
        return json.loads((resource_dir()/"translations"/f"{code}.json").read_text(encoding="utf-8"))

    def set_language(self, code: str) -> None:
        if code not in self.names:
            code = "fr"
        self.language = code
        self.data = self._load(code)

    def text(self, key: str, **values) -> str:
        template = self.data.get(key, self.fallback.get(key, key))
        return template.format(**values)


def load_settings_data() -> dict:
    try:
        data = json.loads(settings_path().read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_settings_data(data: dict) -> None:
    settings_path().write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_language() -> str:
    return str(load_settings_data().get("language", "fr"))


def save_language(code: str) -> None:
    data = load_settings_data()
    data["language"] = code
    save_settings_data(data)


def load_output_directory() -> Path | None:
    data = load_settings_data()
    raw = str(data.get("output_directory", "")).strip()
    if not raw:
        return None

    directory = Path(raw)
    if directory.is_dir():
        return directory

    # Le dossier n'existe plus : retour automatique au comportement d'origine.
    data.pop("output_directory", None)
    save_settings_data(data)
    return None


def save_output_directory(directory: Path | None) -> None:
    data = load_settings_data()
    if directory is None:
        data.pop("output_directory", None)
    else:
        data["output_directory"] = str(directory)
    save_settings_data(data)


def load_business_groups() -> dict[str, BusinessGroup]:
    defaults = clone_default_business_groups()
    raw_groups = load_settings_data().get("business_groups", {})

    if not isinstance(raw_groups, dict):
        return defaults

    result: dict[str, BusinessGroup] = {}
    for key, default in defaults.items():
        raw = raw_groups.get(key, {})
        if not isinstance(raw, dict):
            result[key] = default
            continue

        title = str(raw.get("title", "")).strip()
        custom = bool(raw.get("title_custom", False)) and bool(title)
        result[key] = BusinessGroup(
            key=key,
            title=title if custom else "",
            title_custom=custom,
        )

    return result


def save_business_groups(groups: dict[str, BusinessGroup]) -> None:
    data = load_settings_data()
    data["business_groups"] = {
        key: asdict(group)
        for key, group in groups.items()
    }
    save_settings_data(data)


def load_presets() -> dict[str, list[Preset]]:
    if not presets_path().exists():
        return clone_defaults()
    try:
        raw = json.loads(presets_path().read_text(encoding="utf-8"))
        result: dict[str, list[Preset]] = {}
        for group in ("wordpress", "prestashop"):
            items = raw.get(group, [])
            if len(items) != 4:
                raise ValueError("Invalid preset count")
            parsed: list[Preset] = []
            for item in items:
                key = str(item["key"])
                title = str(item.get("title", "")).strip()
                custom = bool(item.get("title_custom", title not in LEGACY_DEFAULT_TITLES.get(key, set())))
                parsed.append(Preset(
                    key=key, title=title if custom else "", title_custom=custom,
                    width=int(item["width"]), height=item.get("height"),
                    quality=int(item["quality"]), mode=str(item["mode"]),
                ))
            result[group] = parsed
        return result
    except Exception:
        return clone_defaults()


def save_presets(presets: dict[str, list[Preset]]) -> None:
    payload = {group: [asdict(item) for item in items] for group, items in presets.items()}
    presets_path().write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


class ConversionWorker(QObject):
    progress = Signal(int, int, str)
    completed = Signal(list)
    failed = Signal(str)

    def __init__(
        self,
        files: list[Path],
        preset: Preset,
        output_dir: Path | None,
    ):
        super().__init__()
        self.files = files
        self.preset = preset
        self.output_dir = output_dir

    def run(self) -> None:
        results = []
        try:
            total = len(self.files)
            for index, source in enumerate(self.files, 1):
                self.progress.emit(index-1, total, source.name)
                try:
                    dest, before, after = convert_one(source, self.preset, self.output_dir)
                    results.append({"source":source,"destination":dest,"before":before,"after":after,"error":None})
                except Exception as exc:
                    results.append({"source":source,"destination":None,"before":0,"after":0,"error":str(exc)})
                self.progress.emit(index, total, source.name)
            self.completed.emit(results)
        except Exception as exc:
            self.failed.emit(str(exc))


class Toast(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName("toast")
        self.setFixedWidth(430)
        self.hide()
        layout = QHBoxLayout(self); layout.setContentsMargins(15,12,10,12); layout.setSpacing(11)
        self.icon = QLabel("✓"); self.icon.setObjectName("toastIcon"); self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter); self.icon.setFixedSize(32,32)
        text = QVBoxLayout(); text.setSpacing(2)
        self.title = QLabel(""); self.title.setObjectName("toastTitle")
        self.message = QLabel(""); self.message.setObjectName("toastMessage"); self.message.setWordWrap(True)
        text.addWidget(self.title); text.addWidget(self.message)
        close = QPushButton("×"); close.setObjectName("toastClose"); close.setFixedSize(28,28); close.clicked.connect(self.hide)
        layout.addWidget(self.icon); layout.addLayout(text,1); layout.addWidget(close)
        self.timer = QTimer(self); self.timer.setSingleShot(True); self.timer.timeout.connect(self.hide)

    def show_message(self, title: str, message: str, kind="success", timeout=4200):
        self.icon.setText({"success":"✓","warning":"!","error":"×","info":"i"}.get(kind,"i"))
        self.title.setText(title); self.message.setText(message); self.adjustSize(); self.show(); self.raise_(); self.timer.start(timeout)


class NoWheelComboBox(QComboBox):
    """Empêche la roulette de changer une sélection par accident."""
    def wheelEvent(self, event):
        event.ignore()


class ElidedLabel(QLabel):
    """Affiche un texte long sans casser la mise en page."""

    def __init__(self, text: str = ""):
        super().__init__("")
        self._full_text = text

    def setFullText(self, text: str) -> None:
        self._full_text = str(text)
        self.setToolTip(self._full_text)
        self._refresh_elision()

    def _refresh_elision(self) -> None:
        available = max(80, self.width() - 4)
        display = self.fontMetrics().elidedText(
            self._full_text,
            Qt.TextElideMode.ElideMiddle,
            available,
        )
        super().setText(display)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._refresh_elision()


class BenefitRow(QWidget):
    def __init__(self, icon_path: Path):
        super().__init__()
        layout = QHBoxLayout(self); layout.setContentsMargins(0,0,0,0); layout.setSpacing(10)
        icon = QLabel(); icon.setFixedSize(24,24)
        pix = QPixmap(str(icon_path)); icon.setPixmap(pix.scaled(24,24,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
        self.label = QLabel(""); self.label.setObjectName("benefitText")
        layout.addWidget(icon); layout.addWidget(self.label,1)


class ModeCard(QFrame):
    """Sélecteur métier avec une hiérarchie typographique claire."""
    clicked = Signal(str)

    def __init__(self, mode: str):
        super().__init__()
        self.mode = mode
        self.setObjectName("modeCard")
        self.setProperty("selected", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(88)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 13, 18, 13)
        layout.setSpacing(3)

        self.title = QLabel("")
        self.title.setObjectName("modeTitle")
        self.description = QLabel("")
        self.description.setObjectName("modeDescription")
        self.description.setWordWrap(True)

        layout.addWidget(self.title)
        layout.addWidget(self.description)
        layout.addStretch()

    def set_texts(self, title: str, description: str) -> None:
        self.title.setText(title)
        self.description.setText(description)

    def set_selected(self, selected: bool) -> None:
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.mode)
        super().mousePressEvent(event)


class DropZone(QFrame):
    files_dropped = Signal(list)
    result_finished = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("dropZone")
        self.setAcceptDrops(True)
        self.setMinimumHeight(258)
        self.setMaximumHeight(286)
        self.setProperty("resultKind", "")
        self._destination_full_text = ""

        self.result_timer = QTimer(self)
        self.result_timer.setSingleShot(True)
        self.result_timer.timeout.connect(self._finish_result)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        self.stack.setObjectName("dropStack")
        outer.addWidget(self.stack)

        self.default_page = QWidget()
        default_layout = QVBoxLayout(self.default_page)
        default_layout.setContentsMargins(24, 20, 24, 20)
        default_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        default_layout.setSpacing(9)

        self.title = QLabel("")
        self.title.setObjectName("dropTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.description = QLabel("")
        self.description.setObjectName("dropDescription")
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description.setWordWrap(True)

        self.destination_bar = QFrame()
        self.destination_bar.setObjectName("destinationBar")
        destination_layout = QHBoxLayout(self.destination_bar)
        destination_layout.setContentsMargins(13, 5, 5, 5)
        destination_layout.setSpacing(7)

        self.destination_label = QLabel("")
        self.destination_label.setObjectName("destinationLabel")
        self.destination_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        self.destination_button = QPushButton("")
        self.destination_button.setObjectName("destinationButton")
        self.destination_button.setMinimumHeight(34)

        self.reset_destination_button = QPushButton("")
        self.reset_destination_button.setObjectName("resetDestinationButton")
        self.reset_destination_button.setMinimumHeight(34)
        self.reset_destination_button.hide()

        destination_layout.addWidget(self.destination_label, 1)
        destination_layout.addWidget(self.destination_button)
        destination_layout.addWidget(self.reset_destination_button)

        self.choose_button = QPushButton("")
        self.choose_button.setObjectName("primaryButton")
        self.choose_button.setFixedWidth(224)

        default_layout.addStretch(1)
        default_layout.addWidget(self.title)
        default_layout.addWidget(self.description)
        default_layout.addSpacing(5)
        default_layout.addWidget(
            self.destination_bar,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        default_layout.addSpacing(5)
        default_layout.addWidget(
            self.choose_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        default_layout.addStretch(1)

        self.result_page = QWidget()
        self.result_page.setObjectName("dropResultPage")
        result_layout = QVBoxLayout(self.result_page)
        result_layout.setContentsMargins(24, 20, 24, 20)
        result_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.setSpacing(8)

        self.result_icon = QLabel("✓")
        self.result_icon.setObjectName("dropResultIcon")
        self.result_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_icon.setFixedSize(62, 62)

        self.result_title = QLabel("")
        self.result_title.setObjectName("dropResultTitle")
        self.result_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.result_message = QLabel("")
        self.result_message.setObjectName("dropResultMessage")
        self.result_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_message.setWordWrap(True)

        result_layout.addStretch(1)
        result_layout.addWidget(
            self.result_icon,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        result_layout.addWidget(self.result_title)
        result_layout.addWidget(self.result_message)
        result_layout.addStretch(1)

        self.stack.addWidget(self.default_page)
        self.stack.addWidget(self.result_page)
        self.stack.setCurrentWidget(self.default_page)

    def set_destination(self, text: str, custom: bool) -> None:
        self._destination_full_text = text
        self.destination_label.setToolTip(text)
        self.reset_destination_button.setVisible(custom)
        QTimer.singleShot(0, self._update_destination_elision)

    def _update_destination_elision(self) -> None:
        width = max(150, self.destination_label.width() - 4)
        text = self.destination_label.fontMetrics().elidedText(
            self._destination_full_text,
            Qt.TextElideMode.ElideMiddle,
            width,
        )
        self.destination_label.setText(text)

    def show_default(self) -> None:
        self.result_timer.stop()
        self.stack.setCurrentWidget(self.default_page)
        self.setProperty("resultKind", "")
        self.style().unpolish(self)
        self.style().polish(self)

    def show_result(
        self,
        title: str,
        message: str,
        kind: str = "success",
        duration: int = 5000,
    ) -> None:
        self.result_timer.stop()
        self.result_title.setText(title)
        self.result_message.setText(message)
        self.result_icon.setText("✓" if kind == "success" else "!")
        self.setProperty("resultKind", kind)
        self.result_icon.setProperty("resultKind", kind)
        self.style().unpolish(self)
        self.style().polish(self)
        self.result_icon.style().unpolish(self.result_icon)
        self.result_icon.style().polish(self.result_icon)
        self.stack.setCurrentWidget(self.result_page)
        self.result_timer.start(duration)

    def _finish_result(self) -> None:
        self.show_default()
        self.result_finished.emit()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Barre centrée, compacte et limitée à environ la moitié de la zone.
        destination_width = min(
            500,
            max(340, int(self.width() * 0.48)),
        )
        self.destination_bar.setFixedWidth(destination_width)
        self._update_destination_elision()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragActive", True)
            self.style().unpolish(self)
            self.style().polish(self)

    def dragLeaveEvent(self, event):
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        event.accept()

    def dropEvent(self, event):
        self.setProperty("dragActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.files_dropped.emit(
            [url.toLocalFile() for url in event.mimeData().urls()]
        )
        event.acceptProposedAction()


class PresetCard(QFrame):
    clicked = Signal(object)

    def __init__(self, preset: Preset, tr: Translator):
        super().__init__()
        self.preset = preset
        self.tr = tr
        self.setObjectName("presetCard")
        self.setProperty("selected", False)
        # Hauteur validée : elle ne doit plus être réduite.
        self.setFixedHeight(124)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        self.radio = QRadioButton("")
        self.radio.setObjectName("presetRadio")
        self.radio.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        dimensions_row = QHBoxLayout()
        dimensions_row.setContentsMargins(0, 0, 0, 0)
        dimensions_row.setSpacing(7)

        self.size_label = QLabel("")
        self.size_label.setObjectName("presetSize")
        self.mode_label = QLabel("")
        self.mode_label.setObjectName("presetMode")

        dimensions_row.addWidget(self.size_label)
        dimensions_row.addWidget(
            self.mode_label,
            alignment=Qt.AlignmentFlag.AlignBottom,
        )
        dimensions_row.addStretch()

        self.detail_label = QLabel("")
        self.detail_label.setObjectName("presetDetail")

        layout.addWidget(self.radio)
        layout.addLayout(dimensions_row)
        layout.addWidget(self.detail_label)
        layout.addStretch()
        self.retranslate()

    def retranslate(self):
        self.radio.setText(self.preset.display_title(self.tr))
        if self.preset.mode == "long_edge":
            size = f"{self.preset.width} px"
            mode_key = "card_mode_long_edge"
        else:
            size = f"{self.preset.width} × {self.preset.height} px"
            mode_key = (
                "card_mode_contain"
                if self.preset.mode == "contain"
                else "card_mode_cover"
            )

        self.size_label.setText(size)
        self.mode_label.setText("· " + self.tr.text(mode_key))
        self.detail_label.setText(
            self.tr.text(
                "quality_label",
                quality=self.preset.quality,
            )
        )

    def mousePressEvent(self, event):
        self.clicked.emit(self.preset)
        super().mousePressEvent(event)

    def set_selected(self, selected):
        self.radio.setChecked(selected)
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)


class PresetEditorCard(QFrame):
    def __init__(self, preset: Preset, tr: Translator, index: int):
        super().__init__()
        self.preset=preset; self.tr=tr; self.index=index; self.setObjectName("editorCard")
        layout=QVBoxLayout(self); layout.setContentsMargins(16,16,16,16); layout.setSpacing(12)
        self.heading=QLabel(""); self.heading.setObjectName("editorHeading"); layout.addWidget(self.heading)
        self.form=QFormLayout(); self.form.setSpacing(9)

        self.title_input=QLineEdit(preset.display_title(tr)); self.title_input.setObjectName("settingsInput")
        self.width_input=self._number_input(preset.width,100,10000)
        self.height_input=self._number_input(preset.height or preset.width,100,10000)
        self.quality_input=self._number_input(preset.quality,1,100)
        self.mode_input=NoWheelComboBox(); self.mode_input.setObjectName("settingsCombo")
        self.mode_input.currentIndexChanged.connect(self._update_height_state)

        for widget in (self.title_input,self.width_input,self.height_input,self.quality_input,self.mode_input):
            self.form.addRow("",widget)
        layout.addLayout(self.form)
        self.retranslate()
        self._update_height_state()

    @staticmethod
    def _number_input(value:int, minimum:int, maximum:int) -> QLineEdit:
        field=QLineEdit(str(value))
        field.setObjectName("settingsNumber")
        field.setValidator(QIntValidator(minimum,maximum,field))
        field.setAlignment(Qt.AlignmentFlag.AlignRight)
        field.setClearButtonEnabled(True)
        return field

    def _label_for(self,row):
        item=self.form.itemAt(row,QFormLayout.ItemRole.LabelRole)
        return item.widget() if item else None

    def retranslate(self):
        self.heading.setText(self.tr.text("card_number",number=self.index+1))
        for row,key in enumerate(("field_name","field_width","field_height","field_quality","field_mode")):
            label=self._label_for(row)
            if label: label.setText(self.tr.text(key))
        current=self.mode_input.currentData() or self.preset.mode
        self.mode_input.blockSignals(True)
        self.mode_input.clear()
        self.mode_input.addItem(self.tr.text("mode_long_edge"),"long_edge")
        self.mode_input.addItem(self.tr.text("mode_contain"),"contain")
        self.mode_input.addItem(self.tr.text("mode_cover"),"cover")
        self.mode_input.setCurrentIndex(max(0,self.mode_input.findData(current)))
        self.mode_input.blockSignals(False)
        if not self.preset.title_custom:
            self.title_input.setText(self.preset.display_title(self.tr))

    def _update_height_state(self):
        self.height_input.setEnabled(self.mode_input.currentData()!="long_edge")

    @staticmethod
    def _read_number(field:QLineEdit, fallback:int, minimum:int, maximum:int) -> int:
        try:
            value=int(field.text().strip())
        except ValueError:
            value=fallback
        value=max(minimum,min(maximum,value))
        field.setText(str(value))
        return value

    def to_preset(self):
        entered=self.title_input.text().strip()
        default=self.tr.text(PRESET_TITLE_KEYS[self.preset.key])
        custom=entered!=default
        width=self._read_number(self.width_input,self.preset.width,100,10000)
        height=self._read_number(self.height_input,self.preset.height or self.preset.width,100,10000)
        quality=self._read_number(self.quality_input,self.preset.quality,1,100)
        mode=str(self.mode_input.currentData())
        return Preset(
            self.preset.key,
            entered if custom else "",
            custom,
            width,
            None if mode=="long_edge" else height,
            quality,
            mode,
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language=load_language(); self.tr=Translator(self.language)
        self.setWindowTitle(APP_NAME); self.setMinimumSize(1040,660)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint,False)
        icon=app_icon_path()
        if icon.exists():
            self.setWindowIcon(QIcon(str(icon)))
        self.presets=load_presets()
        self.business_groups=load_business_groups()
        self.mode="wordpress"
        self.selected_preset=self.presets["wordpress"][2]
        self.preset_cards=[]
        self.editor_cards={"wordpress":[],"prestashop":[]}
        self.business_name_inputs={}
        self.business_name_defaults={}
        self.output_directory=load_output_directory()
        self.active_output_directory=None
        self.thread=None
        self.worker=None
        self._build_ui(); self._apply_styles(); self._render_presets(); self._render_settings(); self.toast=Toast(self); self._retranslate_ui(); QTimer.singleShot(0,self._fit_window_to_screen)

    def _build_ui(self):
        central=QWidget(); central.setObjectName("root"); self.setCentralWidget(central)
        root=QHBoxLayout(central); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        sidebar=QFrame(); sidebar.setObjectName("sidebar"); sidebar.setFixedWidth(240)
        side=QVBoxLayout(sidebar); side.setContentsMargins(18,20,18,18); side.setSpacing(8)
        logo=QLabel(); logo.setObjectName("brandLogo"); logo.setFixedHeight(78); logo.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        pix=QPixmap(str(resource_dir()/"assets"/"brand"/"2Webp-logo-exact.png")); logo.setPixmap(pix.scaled(196,76,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
        side.addWidget(logo); side.addSpacing(15)
        self.convert_nav=QPushButton(""); self.settings_nav=QPushButton("")
        for button in (self.convert_nav,self.settings_nav): button.setObjectName("navButton"); button.setCheckable(True); button.setMinimumHeight(44)
        self.convert_nav.setChecked(True); group=QButtonGroup(self); group.setExclusive(True); group.addButton(self.convert_nav); group.addButton(self.settings_nav)
        self.convert_nav.clicked.connect(lambda:self._show_page(0)); self.settings_nav.clicked.connect(lambda:self._show_page(1))
        side.addWidget(self.convert_nav)

        # Un seul bouton Languages. La langue active n'est jamais affichée en permanence.
        side.addSpacing(10)
        self.language_button=QPushButton("Languages")
        self.language_button.setObjectName("languageButton")
        self.language_button.setMinimumHeight(44)
        self.language_menu=QMenu(self.language_button)
        self.language_menu.setObjectName("languageMenu")
        self.language_button.setMenu(self.language_menu)
        self._build_language_menu()
        side.addWidget(self.language_button)

        side.addSpacing(10)
        side.addWidget(self.settings_nav)
        side.addStretch()
        benefits=QFrame(); benefits.setObjectName("benefitsBox"); bl=QVBoxLayout(benefits); bl.setContentsMargins(13,13,13,13); bl.setSpacing(10)
        self.benefit_rows=[]
        for name in ("benefit-speed.png","benefit-quality.png","benefit-local.png","benefit-light.png"):
            row=BenefitRow(resource_dir()/"assets"/"icons"/name); self.benefit_rows.append(row); bl.addWidget(row)
        side.addWidget(benefits)
        self.privacy=QLabel(""); self.privacy.setObjectName("privacyBox"); self.privacy.setWordWrap(True); side.addWidget(self.privacy)
        footer=QLabel(f"jpbloch.fr · 2026 · v{APP_VERSION}"); footer.setObjectName("appFooter"); footer.setAlignment(Qt.AlignmentFlag.AlignCenter); side.addWidget(footer)
        root.addWidget(sidebar)
        self.pages=QStackedWidget(); self.pages.setObjectName("pages"); self.pages.addWidget(self._build_convert_page()); self.pages.addWidget(self._build_settings_page()); root.addWidget(self.pages,1)

    def _build_convert_page(self):
        page = QWidget()
        page.setObjectName("convertPage")
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setObjectName("convertScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        content = QWidget()
        content.setObjectName("content")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(34, 8, 34, 12)
        layout.setSpacing(0)

        # Bloc éditorial volontairement compact.
        hero_block = QWidget()
        hero_block.setObjectName("heroBlock")
        hero_layout = QVBoxLayout(hero_block)
        hero_layout.setContentsMargins(0, 0, 0, 0)
        hero_layout.setSpacing(2)

        self.hero_eyebrow = QLabel("")
        self.hero_eyebrow.setObjectName("eyebrow")
        self.hero_title = QLabel("")
        self.hero_title.setObjectName("title")
        self.hero_subtitle = QLabel("")
        self.hero_subtitle.setObjectName("subtitle")

        hero_layout.addWidget(self.hero_eyebrow)
        hero_layout.addSpacing(1)
        hero_layout.addWidget(self.hero_title)
        hero_layout.addWidget(self.hero_subtitle)
        layout.addWidget(hero_block)

        layout.addSpacing(13)

        modes = QHBoxLayout()
        modes.setSpacing(12)
        self.wp_button = ModeCard("wordpress")
        self.ps_button = ModeCard("prestashop")
        self.wp_button.set_selected(True)
        self.wp_button.clicked.connect(self._set_mode)
        self.ps_button.clicked.connect(self._set_mode)
        modes.addWidget(self.wp_button)
        modes.addWidget(self.ps_button)
        layout.addLayout(modes)

        # Le titre d’usage est directement rattaché aux presets.
        layout.addSpacing(8)
        self.preset_label = QLabel("")
        self.preset_label.setObjectName("sectionLabel")
        layout.addWidget(self.preset_label)

        layout.addSpacing(3)
        self.preset_widget = QWidget()
        self.preset_grid = QGridLayout(self.preset_widget)
        self.preset_grid.setContentsMargins(0, 0, 0, 0)
        self.preset_grid.setHorizontalSpacing(12)
        layout.addWidget(self.preset_widget)

        # Séparation nette entre le choix technique et l’action de conversion.
        layout.addSpacing(18)

        self.drop_zone = DropZone()
        self.drop_zone.choose_button.clicked.connect(self._choose_files)
        self.drop_zone.destination_button.clicked.connect(
            self._choose_destination
        )
        self.drop_zone.reset_destination_button.clicked.connect(
            self._reset_destination
        )
        self.drop_zone.files_dropped.connect(self._receive_paths)
        self.drop_zone.result_finished.connect(self._update_status)
        layout.addWidget(self.drop_zone)

        scroll.setWidget(content)
        page_layout.addWidget(scroll, 1)

        footer = QFrame()
        footer.setObjectName("conversionFooter")
        footer.setFixedHeight(50)

        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(0)

        self.progress = QProgressBar()
        self.progress.setObjectName("progress")
        self.progress.setVisible(False)
        self.progress.setTextVisible(False)
        footer_layout.addWidget(self.progress)

        summary_row = QWidget()
        summary_layout = QHBoxLayout(summary_row)
        summary_layout.setContentsMargins(18, 0, 18, 0)
        summary_layout.setSpacing(9)

        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("footerDot")
        self.status_dot.setFixedWidth(14)
        self.status_dot.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status = ElidedLabel("")
        self.status.setObjectName("footerStatus")
        self.status.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        summary_layout.addWidget(self.status_dot)
        summary_layout.addWidget(self.status, 1)
        footer_layout.addWidget(summary_row, 1)

        page_layout.addWidget(footer)
        return page

    def _build_settings_page(self):
        page=QWidget(); page.setObjectName("settingsPage")
        page_layout=QVBoxLayout(page); page_layout.setContentsMargins(0,0,0,0); page_layout.setSpacing(0)

        header=QWidget(); header.setObjectName("settingsHeader")
        header_layout=QVBoxLayout(header); header_layout.setContentsMargins(34,25,34,16); header_layout.setSpacing(8)
        self.settings_eyebrow=QLabel(""); self.settings_eyebrow.setObjectName("eyebrow")
        self.settings_title=QLabel(""); self.settings_title.setObjectName("title")
        self.settings_subtitle=QLabel(""); self.settings_subtitle.setObjectName("subtitle"); self.settings_subtitle.setWordWrap(True)
        header_layout.addWidget(self.settings_eyebrow)
        header_layout.addWidget(self.settings_title)
        header_layout.addWidget(self.settings_subtitle)
        page_layout.addWidget(header)

        self.settings_scroll=QScrollArea(); self.settings_scroll.setObjectName("settingsCardsScroll")
        self.settings_scroll.setWidgetResizable(True)
        self.settings_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.settings_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.settings_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        content=QWidget(); content.setObjectName("settingsCardsContent")
        content_layout=QVBoxLayout(content); content_layout.setContentsMargins(34,8,26,24); content_layout.setSpacing(0)
        self.settings_sections=QWidget()
        self.settings_sections_layout=QVBoxLayout(self.settings_sections)
        self.settings_sections_layout.setContentsMargins(0,0,0,0)
        self.settings_sections_layout.setSpacing(22)
        content_layout.addWidget(self.settings_sections)
        content_layout.addStretch()
        self.settings_scroll.setWidget(content)
        page_layout.addWidget(self.settings_scroll,1)

        action_bar=QFrame(); action_bar.setObjectName("settingsActionBar"); action_bar.setFixedHeight(74)
        actions=QHBoxLayout(action_bar); actions.setContentsMargins(34,12,34,12); actions.setSpacing(14)
        self.reset_button=QPushButton(""); self.reset_button.setObjectName("resetSettingsButton")
        self.reset_button.setMinimumHeight(46); self.reset_button.setMinimumWidth(235)
        self.reset_button.clicked.connect(self._reset_settings)
        self.save_button=QPushButton(""); self.save_button.setObjectName("saveSettingsButton")
        self.save_button.setMinimumHeight(46); self.save_button.setMinimumWidth(210)
        self.save_button.clicked.connect(self._save_settings)
        actions.addWidget(self.reset_button)
        actions.addStretch()
        actions.addWidget(self.save_button)
        page_layout.addWidget(action_bar)
        return page

    def _business_display_name(self, group: str) -> str:
        return self.business_groups[group].display_title(self.tr)

    def _choose_usage_text(self) -> str:
        return self.tr.text(
            "choose_usage",
            name=self._business_display_name(self.mode),
        )

    def _render_settings(self):
        while self.settings_sections_layout.count():
            item=self.settings_sections_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.editor_cards={"wordpress":[],"prestashop":[]}
        self.business_name_inputs={}
        self.business_name_defaults={}

        names_card=QFrame()
        names_card.setObjectName("businessNamesCard")
        names_layout=QVBoxLayout(names_card)
        names_layout.setContentsMargins(18,16,18,18)
        names_layout.setSpacing(6)

        names_title=QLabel(self.tr.text("business_names_title"))
        names_title.setObjectName("businessNamesTitle")
        names_description=QLabel(self.tr.text("business_names_desc"))
        names_description.setObjectName("businessNamesDescription")
        names_description.setWordWrap(True)
        names_layout.addWidget(names_title)
        names_layout.addWidget(names_description)
        names_layout.addSpacing(8)

        names_grid=QGridLayout()
        names_grid.setContentsMargins(0,0,0,0)
        names_grid.setHorizontalSpacing(14)
        names_grid.setVerticalSpacing(6)

        for column,group in enumerate(("wordpress","prestashop")):
            label=QLabel(self.tr.text(f"business_name_{column+1}"))
            label.setObjectName("businessNameLabel")
            field=QLineEdit(self._business_display_name(group))
            field.setObjectName("businessNameInput")
            field.setClearButtonEnabled(True)
            field.setMaxLength(40)

            self.business_name_inputs[group]=field
            self.business_name_defaults[group]=self.tr.text(GROUP_TITLE_KEYS[group])

            names_grid.addWidget(label,0,column)
            names_grid.addWidget(field,1,column)

        names_layout.addLayout(names_grid)
        self.settings_sections_layout.addWidget(names_card)

        for group in ("wordpress","prestashop"):
            title=QLabel(self._business_display_name(group))
            title.setObjectName("settingsSectionTitle")
            self.settings_sections_layout.addWidget(title)

            widget=QWidget()
            grid=QGridLayout(widget)
            grid.setContentsMargins(0,0,0,0)
            grid.setHorizontalSpacing(12)
            grid.setVerticalSpacing(12)

            for index,preset in enumerate(self.presets[group]):
                editor=PresetEditorCard(preset,self.tr,index)
                self.editor_cards[group].append(editor)
                grid.addWidget(editor,index//2,index%2)

            self.settings_sections_layout.addWidget(widget)

    def _collect_settings(self):
        return {
            group:[editor.to_preset() for editor in self.editor_cards[group]]
            for group in ("wordpress","prestashop")
        }

    def _collect_business_groups(self) -> dict[str, BusinessGroup]:
        result: dict[str, BusinessGroup] = {}

        for group in ("wordpress","prestashop"):
            field=self.business_name_inputs.get(group)
            default=self.business_name_defaults.get(
                group,
                self.tr.text(GROUP_TITLE_KEYS[group]),
            )
            entered=field.text().strip() if field else self._business_display_name(group)

            if not entered:
                entered=default
                if field:
                    field.setText(default)

            custom=entered != default
            result[group]=BusinessGroup(
                key=group,
                title=entered if custom else "",
                title_custom=custom,
            )

        return result
    def _restore_selected(self):
        key=self.selected_preset.key; self.selected_preset=next((p for p in self.presets[self.mode] if p.key==key),self.presets[self.mode][0])
    def _save_settings(self):
        self.presets=self._collect_settings()
        self.business_groups=self._collect_business_groups()
        save_presets(self.presets)
        save_business_groups(self.business_groups)
        self._restore_selected()
        self._render_presets()
        self._render_settings()
        self._retranslate_ui()
        self._show_toast(
            self.tr.text("saved_title"),
            self.tr.text("saved_text"),
            "success",
        )

    def _reset_settings(self):
        self.presets=clone_defaults()
        self.business_groups=clone_default_business_groups()
        save_presets(self.presets)
        save_business_groups(self.business_groups)
        self.selected_preset=self.presets[self.mode][0]
        self._render_settings()
        self._render_presets()
        self._retranslate_ui()
        self._show_toast(
            self.tr.text("reset_title"),
            self.tr.text("reset_text"),
            "info",
        )
    def _build_language_menu(self):
        self.language_menu.clear()
        for code,name in self.tr.names.items():
            action=self.language_menu.addAction(name)
            action.setCheckable(True)
            action.setChecked(code==self.language)
            action.triggered.connect(lambda checked=False, selected=code: self._change_language(selected))

    def _change_language(self, code):
        code=str(code)
        if not code or code==self.language: return
        if self.editor_cards["wordpress"]:
            self.presets=self._collect_settings()
            self.business_groups=self._collect_business_groups()
            self._restore_selected()
        self.language=code
        self.tr.set_language(code)
        save_language(code)
        self._build_language_menu()
        self._render_presets()
        self._render_settings()
        self.drop_zone.show_default()
        self._retranslate_ui()
    def _retranslate_ui(self):
        self.convert_nav.setText("⌂   "+self.tr.text("nav_convert")); self.settings_nav.setText("⚙   "+self.tr.text("nav_settings"))
        for row,key in zip(self.benefit_rows,("benefit_fast","benefit_quality","benefit_local","benefit_light")): row.label.setText(self.tr.text(key))
        self.privacy.setText(f"<b>{self.tr.text('privacy_title')}</b><br>{self.tr.text('privacy_text')}")
        self.hero_eyebrow.setText(self.tr.text("hero_eyebrow"))
        self.hero_title.setText(self.tr.text("hero_title"))
        self.hero_subtitle.setText(self.tr.text("hero_subtitle"))
        self.wp_button.set_texts(
            self._business_display_name("wordpress"),
            self.tr.text("wp_desc"),
        )
        self.ps_button.set_texts(
            self._business_display_name("prestashop"),
            self.tr.text("ps_desc"),
        )
        self.drop_zone.title.setText(self.tr.text("drop_title"))
        self.drop_zone.description.setText(self.tr.text("drop_desc"))
        self.drop_zone.choose_button.setText(self.tr.text("choose_files"))
        self.drop_zone.destination_button.setText(
            self.tr.text("choose_destination")
        )
        self.drop_zone.reset_destination_button.setText(
            self.tr.text("reset_destination")
        )
        self._update_destination_display()
        self.settings_eyebrow.setText(self.tr.text("settings_eyebrow")); self.settings_title.setText(self.tr.text("settings_title")); self.settings_subtitle.setText(self.tr.text("settings_subtitle")); self.reset_button.setText(self.tr.text("reset_defaults")); self.save_button.setText(self.tr.text("save_settings"))
        self.preset_label.setText(self._choose_usage_text())
        self._update_status()
    def _show_page(self,index): self.pages.setCurrentIndex(index)
    def _set_mode(self,mode):
        self.mode=mode
        self.selected_preset=self.presets[mode][0]
        self.wp_button.set_selected(mode=="wordpress")
        self.ps_button.set_selected(mode=="prestashop")
        self.preset_label.setText(self._choose_usage_text())
        self._render_presets()
    def _render_presets(self):
        while self.preset_grid.count():
            item=self.preset_grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self.preset_cards=[]
        for index,preset in enumerate(self.presets[self.mode]):
            card=PresetCard(preset,self.tr); card.clicked.connect(self._select_preset); card.set_selected(preset.key==self.selected_preset.key); self.preset_cards.append(card); self.preset_grid.addWidget(card,0,index)
        self._update_status()
    def _select_preset(self,preset):
        self.selected_preset=preset
        for card in self.preset_cards: card.set_selected(card.preset.key==preset.key)
        self._update_status()
    def _export_size_text(self) -> str:
        if self.selected_preset.mode == "long_edge":
            return f"{self.selected_preset.width} px"
        return (
            f"{self.selected_preset.width} × "
            f"{self.selected_preset.height} px"
        )

    def _preset_mode_text(self) -> str:
        key = {
            "long_edge": "card_mode_long_edge",
            "contain": "card_mode_contain",
            "cover": "card_mode_cover",
        }.get(self.selected_preset.mode, "card_mode_long_edge")
        return self.tr.text(key)

    def _status_destination_value(self) -> str:
        if self.output_directory is None:
            return self.tr.text("destination_default_value")
        return str(self.output_directory)

    def _set_status_text(self, text: str) -> None:
        self.status.setFullText(str(text))

    def _update_status(self, prefix=None):
        if prefix is None:
            text = self.tr.text(
                "status_ready_format",
                size=self._export_size_text(),
                mode=self._preset_mode_text(),
                quality=self.selected_preset.quality,
                destination=self._status_destination_value(),
            )
        else:
            text = str(prefix)
        self._set_status_text(text)

    def _destination_text(self, directory: Path | None = None) -> str:
        active = self.output_directory if directory is None else directory
        if active is None:
            return self.tr.text("destination_default")
        return self.tr.text("destination_custom", path=str(active))

    def _result_destination_text(self, successes: list[dict]) -> str:
        if self.active_output_directory is not None:
            return self.tr.text(
                "destination_custom",
                path=str(self.active_output_directory),
            )

        parents = sorted({
            str(item["destination"].parent)
            for item in successes
            if item.get("destination") is not None
        })

        if len(parents) == 1:
            return self.tr.text("destination_custom", path=parents[0])
        if len(parents) > 1:
            return self.tr.text(
                "destination_multiple_origins",
                count=len(parents),
            )
        return self.tr.text("destination_default")

    def _update_destination_display(self) -> None:
        self.drop_zone.set_destination(
            self._destination_text(),
            custom=self.output_directory is not None,
        )
        if hasattr(self, "status"):
            self._update_status()

    def _choose_destination(self) -> None:
        initial = self.output_directory or Path.home()
        chosen = QFileDialog.getExistingDirectory(
            self,
            self.tr.text("dialog_choose_destination"),
            str(initial),
        )
        if not chosen:
            return

        directory = Path(chosen)
        if not directory.is_dir():
            return

        self.output_directory = directory
        save_output_directory(directory)
        self._update_destination_display()

    def _reset_destination(self) -> None:
        self.output_directory = None
        save_output_directory(None)
        self._update_destination_display()

    def _validated_output_directory(self) -> Path | None:
        if self.output_directory is None:
            return None
        if self.output_directory.is_dir():
            return self.output_directory

        self.output_directory = None
        save_output_directory(None)
        self._update_destination_display()
        self._show_toast(
            self.tr.text("destination_missing_title"),
            self.tr.text("destination_missing_text"),
            "warning",
        )
        return None

    def _choose_files(self):
        files,_=QFileDialog.getOpenFileNames(self,self.tr.text("dialog_choose"),"","Images (*.jpg *.jpeg *.png)")
        if files: self._receive_paths(files)
    def _receive_paths(self,paths):
        files=iter_image_files(paths)
        if not files: self._show_toast(self.tr.text("no_image_title"),self.tr.text("no_image_text"),"warning"); return
        if self.thread and self.thread.isRunning(): self._show_toast(self.tr.text("busy_title"),self.tr.text("busy_text"),"info"); return
        self._start_conversion(files)
    def _start_conversion(self, files):
        self.active_output_directory = self._validated_output_directory()
        self.progress.setVisible(True)
        self.progress.setRange(0, len(files))
        self.progress.setValue(0)
        self.drop_zone.show_default()
        self.drop_zone.setEnabled(False)
        self._update_status(
            self.tr.text("status_batch", count=len(files))
        )

        self.thread = QThread(self)
        self.worker = ConversionWorker(
            files,
            self.selected_preset,
            self.active_output_directory,
        )
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self._on_progress)
        self.worker.completed.connect(self._on_completed)
        self.worker.failed.connect(self._on_failed)
        self.worker.completed.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)
        self.worker.completed.connect(self.worker.deleteLater)
        self.worker.failed.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def _on_progress(self, current, total, filename):
        self.progress.setRange(0, total)
        self.progress.setValue(current)
        self._set_status_text(
            self.tr.text(
                "status_converting",
                current=current,
                total=total,
                filename=filename,
            )
        )

    def _on_completed(self, results):
        self.drop_zone.setEnabled(True)
        self.progress.setVisible(False)

        successes = [item for item in results if item["error"] is None]
        failures = [item for item in results if item["error"] is not None]
        before = sum(item["before"] for item in successes)
        after = sum(item["after"] for item in successes)
        reduction = max(0, round((1 - after / before) * 100)) if before else 0
        destination = self._result_destination_text(successes)

        if successes:
            self._update_status(
                self.tr.text(
                    "status_done",
                    count=len(successes),
                    reduction=reduction,
                )
            )
            if failures:
                self.drop_zone.show_result(
                    self.tr.text("result_partial_title"),
                    self.tr.text(
                        "result_partial_text",
                        count=len(successes),
                        errors=len(failures),
                        destination=destination,
                    ),
                    "warning",
                    5000,
                )
            else:
                self.drop_zone.show_result(
                    self.tr.text("result_success_title"),
                    self.tr.text(
                        "result_success_text",
                        count=len(successes),
                        reduction=reduction,
                        destination=destination,
                    ),
                    "success",
                    5000,
                )
        else:
            self._update_status(self.tr.text("status_error"))
            self.drop_zone.show_result(
                self.tr.text("result_error_title"),
                self.tr.text(
                    "result_error_text",
                    errors=len(failures),
                ),
                "error",
                6500,
            )

        self.active_output_directory = None

    def _on_failed(self, error):
        self.drop_zone.setEnabled(True)
        self.progress.setVisible(False)
        self._update_status(self.tr.text("status_error"))
        self.drop_zone.show_result(
            self.tr.text("result_error_title"),
            error,
            "error",
            6500,
        )
        self.active_output_directory = None
    def _fit_window_to_screen(self):
        screen=self.screen() or QApplication.primaryScreen()
        if not screen: self.resize(1180,720); return
        available=screen.availableGeometry(); max_w=max(self.minimumWidth(),min(1260,int(available.width()*0.94))); max_h=max(self.minimumHeight(),min(800,int(available.height()*0.92))); self.setMaximumSize(max_w,max_h); self.resize(min(max_w,max(self.minimumWidth(),int(available.width()*0.90))),min(max_h,max(self.minimumHeight(),int(available.height()*0.88)))); frame=self.frameGeometry(); frame.moveCenter(available.center()); self.move(frame.topLeft())
    def changeEvent(self,event):
        super().changeEvent(event)
        if event.type()==QEvent.Type.WindowStateChange and self.windowState() & (Qt.WindowState.WindowMaximized|Qt.WindowState.WindowFullScreen): QTimer.singleShot(0,self._restore_compact)
    def _restore_compact(self): self.setWindowState(Qt.WindowState.WindowNoState); self._fit_window_to_screen()
    def _position_toast(self):
        if not hasattr(self,"toast") or not self.toast.isVisible(): return
        margin=22; self.toast.move(max(margin,self.width()-self.toast.width()-margin),max(margin,self.height()-self.toast.height()-margin)); self.toast.raise_()
    def _show_toast(self,title,message,kind="success",timeout=4200): self.toast.show_message(title,message,kind,timeout); self._position_toast()
    def resizeEvent(self,event): super().resizeEvent(event); self._position_toast()

    def _apply_styles(self):
        self.setStyleSheet(r'''
        * { font-family: "Segoe UI Variable", "Segoe UI"; color: #F4F6FA; }
        QWidget#root, QWidget#content, QWidget#convertPage, QWidget#settingsPage, QWidget#settingsCardsContent, QStackedWidget#pages, QScrollArea { background: #0D0F14; }
        QScrollArea { border: none; }
        QFrame#sidebar { background: #101319; border-right: 1px solid rgba(255,255,255,0.08); }
        QLabel#brandLogo { background: transparent; }
        QPushButton#navButton { border:none; border-radius:12px; text-align:left; padding:0 14px; color:#AEB5C2; background:transparent; font-size:14px; }
        QPushButton#navButton:hover { color:white; background:rgba(255,255,255,0.05); }
        QPushButton#navButton:checked { color:white; background:rgba(255,107,44,0.16); border-left:3px solid #FF6B2C; }
        QPushButton#languageButton {
            border:none;
            border-radius:12px;
            text-align:left;
            padding:0 34px 0 14px;
            color:#AEB5C2;
            background:transparent;
            font-size:14px;
        }
        QPushButton#languageButton:hover, QPushButton#languageButton:pressed {
            color:white;
            background:rgba(255,255,255,0.05);
        }
        QPushButton#languageButton::menu-indicator {
            subcontrol-origin:padding;
            subcontrol-position:center right;
            right:13px;
            width:10px;
            height:10px;
        }
        QMenu#languageMenu {
            min-width:190px;
            background:#171A21;
            color:#F4F6FA;
            border:1px solid #343944;
            border-radius:10px;
            padding:6px;
        }
        QMenu#languageMenu::item {
            min-height:30px;
            padding:4px 28px 4px 12px;
            border-radius:7px;
        }
        QMenu#languageMenu::item:selected {
            background:rgba(255,107,44,0.18);
            color:white;
        }
        QMenu#languageMenu::indicator {
            width:12px;
            height:12px;
            left:8px;
        }
        QFrame#benefitsBox { background:rgba(255,122,0,0.045); border:1px solid rgba(255,122,0,0.14); border-radius:14px; }
        QLabel#benefitText { color:#EDF1F7; font-size:12px; font-weight:650; }
        QLabel#privacyBox { color:#AEB5C2; background:rgba(255,255,255,0.035); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:14px; }
        QLabel#appFooter { color:#747C89; font-size:10px; padding-top:4px; }
        QWidget#heroBlock { background:transparent; }
        QLabel#eyebrow { color:#FF8B58; font-size:12px; font-weight:800; }
        QLabel#title { font-size:30px; font-weight:790; }
        QLabel#subtitle {
            color:#B3BAC6;
            font-size:15px;
            padding:0;
        }
        QFrame#modeCard {
            background:#171A21;
            border:1px solid rgba(255,255,255,0.09);
            border-radius:16px;
        }
        QFrame#modeCard:hover {
            background:#1D212A;
            border:1px solid rgba(255,255,255,0.16);
        }
        QFrame#modeCard[selected="true"] {
            background:rgba(255,107,44,0.11);
            border:1px solid rgba(255,107,44,0.72);
        }
        QLabel#modeTitle {
            color:#F7F8FA;
            font-size:18px;
            font-weight:800;
        }
        QLabel#modeDescription {
            color:#B9C0CD;
            font-size:13px;
        }
        QLabel#sectionLabel {
            color:#F4F6FA;
            font-size:17px;
            font-weight:820;
        }
        QLabel#settingsSectionTitle {
            font-size:15px;
            font-weight:750;
        }
        QFrame#businessNamesCard {
            background:rgba(255,107,44,0.045);
            border:1px solid rgba(255,107,44,0.18);
            border-radius:15px;
        }
        QLabel#businessNamesTitle {
            color:#F7F8FA;
            font-size:15px;
            font-weight:800;
        }
        QLabel#businessNamesDescription {
            color:#AEB5C2;
            font-size:12px;
        }
        QLabel#businessNameLabel {
            color:#C4CAD4;
            font-size:11px;
            font-weight:700;
        }
        QLineEdit#businessNameInput {
            min-height:38px;
            background:#101319;
            border:1px solid rgba(255,255,255,0.12);
            border-radius:9px;
            padding:0 10px;
            font-size:13px;
            font-weight:700;
        }
        QLineEdit#businessNameInput:focus {
            border:1px solid #FF6B2C;
        }
        QFrame#conversionFooter {
            background:#12161D;
            border-top:1px solid rgba(255,107,44,0.24);
        }
        QLabel#footerDot {
            color:#FF6B2C;
            font-size:15px;
            font-weight:900;
        }
        QLabel#footerStatus {
            color:#EEF1F6;
            font-size:13px;
            font-weight:720;
        }
        QFrame#presetCard, QFrame#editorCard { background:#171A21; border:1px solid rgba(255,255,255,0.09); border-radius:15px; }
        QFrame#presetCard:hover { background:#1D212A; border:1px solid rgba(255,255,255,0.17); }
        QFrame#presetCard[selected="true"] { background:rgba(255,107,44,0.10); border:1px solid rgba(255,107,44,0.72); }
        QRadioButton#presetRadio {
            font-size:15px;
            font-weight:780;
            spacing:8px;
        }
        QRadioButton#presetRadio::indicator {
            width:12px;
            height:12px;
            border-radius:7px;
        }
        QRadioButton#presetRadio::indicator:unchecked {
            background:#F4F6FA;
            border:1px solid #F4F6FA;
        }
        QRadioButton#presetRadio::indicator:checked {
            background:#FF6B2C;
            border:1px solid #FF6B2C;
        }
        QLabel#presetSize {
            font-size:25px;
            font-weight:850;
        }
        QLabel#presetMode, QLabel#presetDetail {
            color:#B5BCC8;
            font-size:12px;
            font-weight:650;
        }
        QLabel#editorHeading { color:#FF8B58; font-size:12px; font-weight:800; }
        QLineEdit#settingsInput, QLineEdit#settingsNumber, QComboBox#settingsCombo { min-height:38px; background:#101319; border:1px solid rgba(255,255,255,0.12); border-radius:9px; padding:0 10px; }
        QLineEdit#settingsInput:focus, QLineEdit#settingsNumber:focus, QComboBox#settingsCombo:focus { border:1px solid #FF6B2C; }
        QLineEdit#settingsNumber:disabled { color:#717987; background:#0E1116; border-color:rgba(255,255,255,0.06); }
        QFrame#dropZone {
            background:rgba(255,255,255,0.018);
            border:2px dashed rgba(255,255,255,0.20);
            border-radius:20px;
        }
        QFrame#dropZone[dragActive="true"] {
            background:rgba(255,107,44,0.06);
            border:2px dashed #FF6B2C;
        }
        QFrame#dropZone[resultKind="success"] {
            background:rgba(69,201,132,0.055);
            border:2px solid rgba(91,222,158,0.48);
        }
        QFrame#dropZone[resultKind="warning"] {
            background:rgba(255,174,67,0.055);
            border:2px solid rgba(255,174,67,0.48);
        }
        QFrame#dropZone[resultKind="error"] {
            background:rgba(244,91,105,0.055);
            border:2px solid rgba(244,91,105,0.48);
        }
        QStackedWidget#dropStack, QWidget#dropResultPage {
            background:transparent;
            border:none;
        }
        QLabel#dropTitle {
            font-size:27px;
            font-weight:850;
        }
        QLabel#dropDescription {
            color:#C4CBD5;
            font-size:14px;
            line-height:1.35;
        }
        QFrame#destinationBar {
            background:rgba(255,255,255,0.035);
            border:1px solid rgba(255,255,255,0.09);
            border-radius:11px;
        }
        QLabel#destinationLabel {
            color:#D0D5DE;
            font-size:13px;
            font-weight:680;
        }
        QPushButton#destinationButton {
            border:1px solid rgba(255,255,255,0.13);
            border-radius:8px;
            background:#1A1E26;
            color:#F4F6FA;
            font-size:12px;
            font-weight:740;
            padding:0 12px;
        }
        QPushButton#destinationButton:hover {
            background:#242A35;
            border-color:rgba(255,255,255,0.23);
        }
        QPushButton#resetDestinationButton {
            border:1px solid rgba(255,107,44,0.28);
            border-radius:8px;
            background:rgba(255,107,44,0.10);
            color:#FF9A6C;
            font-size:12px;
            font-weight:780;
            padding:0 12px;
        }
        QPushButton#resetDestinationButton:hover {
            background:rgba(255,107,44,0.18);
            border-color:rgba(255,107,44,0.55);
        }
        QLabel#dropResultIcon {
            color:#7DE2AE;
            background:rgba(74,210,143,0.13);
            border:1px solid rgba(93,226,161,0.32);
            border-radius:29px;
            font-size:30px;
            font-weight:900;
        }
        QLabel#dropResultIcon[resultKind="warning"] {
            color:#FFC56A;
            background:rgba(255,174,67,0.13);
            border-color:rgba(255,174,67,0.32);
        }
        QLabel#dropResultIcon[resultKind="error"] {
            color:#FF7F8D;
            background:rgba(244,91,105,0.13);
            border-color:rgba(244,91,105,0.32);
        }
        QLabel#dropResultTitle {
            color:#F7F8FA;
            font-size:24px;
            font-weight:870;
        }
        QLabel#dropResultMessage {
            color:#CCD2DC;
            font-size:14px;
            font-weight:600;
        }
        QPushButton#primaryButton {
            min-height:48px;
            border:none;
            border-radius:12px;
            background:#F7F8FA;
            color:#111318;
            font-size:16px;
            font-weight:850;
            padding:0 20px;
        }
        QPushButton#secondaryButton {
            min-height:42px;
            border:1px solid rgba(255,255,255,0.14);
            border-radius:12px;
            background:#171A21;
            color:#F4F6FA;
            font-weight:650;
            padding:0 18px;
        }
        QWidget#settingsHeader { background:#0D0F14; border-bottom:1px solid rgba(255,255,255,0.06); }
        QFrame#settingsActionBar { background:#12151B; border-top:1px solid rgba(255,255,255,0.10); }
        QPushButton#resetSettingsButton { border:1px solid rgba(255,255,255,0.22); border-radius:12px; background:#1A1E26; color:#F5F7FA; font-size:13px; font-weight:700; padding:0 20px; }
        QPushButton#resetSettingsButton:hover { background:#232833; border-color:rgba(255,255,255,0.34); }
        QPushButton#resetSettingsButton:pressed { background:#11141A; }
        QPushButton#saveSettingsButton { border:1px solid #FF7A3D; border-radius:12px; background:#FF6B2C; color:white; font-size:13px; font-weight:800; padding:0 22px; }
        QPushButton#saveSettingsButton:hover { background:#FF7A3D; }
        QPushButton#saveSettingsButton:pressed { background:#E9571F; }
        QScrollArea#settingsCardsScroll QScrollBar:vertical { background:#0D0F14; width:12px; margin:5px 2px 5px 0; }
        QScrollArea#settingsCardsScroll QScrollBar::handle:vertical { background:rgba(255,255,255,0.22); min-height:44px; border-radius:5px; }
        QScrollArea#settingsCardsScroll QScrollBar::handle:vertical:hover { background:rgba(255,107,44,0.70); }
        QScrollArea#settingsCardsScroll QScrollBar::add-line:vertical, QScrollArea#settingsCardsScroll QScrollBar::sub-line:vertical { height:0; background:transparent; border:none; }
        QScrollArea#settingsCardsScroll QScrollBar::add-page:vertical, QScrollArea#settingsCardsScroll QScrollBar::sub-page:vertical { background:transparent; }
        QProgressBar#progress {
            min-height:4px;
            max-height:4px;
            border:none;
            border-radius:0;
            background:rgba(255,255,255,0.055);
        }
        QProgressBar#progress::chunk {
            border-radius:0;
            background:#FF6B2C;
        }
        QFrame#toast { background:#191D25; border:1px solid rgba(255,255,255,0.13); border-radius:16px; }
        QLabel#toastIcon { background:rgba(79,209,139,0.13); border-radius:16px; color:#73E2A7; font-size:17px; font-weight:800; }
        QLabel#toastTitle { color:white; font-size:13px; font-weight:750; }
        QLabel#toastMessage { color:#B8BFCC; font-size:12px; }
        QPushButton#toastClose { border:none; border-radius:8px; background:transparent; color:#AEB5C2; font-size:18px; }
        ''')


def main():
    configure_windows_app_identity()
    app=QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setOrganizationName("jpbloch.fr")

    icon=app_icon_path()
    if icon.exists():
        app.setWindowIcon(QIcon(str(icon)))

    window=MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__": main()
