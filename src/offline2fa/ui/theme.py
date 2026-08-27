from string import Template

DARK = {
    "name": "dark",
    "bg": "#0f0f17",
    "surface": "#171724",
    "card": "#1c1c2b",
    "card_hover": "#242438",
    "border": "#2b2b41",
    "input": "#1a1a29",
    "text": "#f2f2f8",
    "muted": "#9292ab",
    "track": "#2d2d45",
    "brand": "#6c5ce7",
    "brand_hover": "#7d6ff2",
    "danger": "#e05561",
}

LIGHT = {
    "name": "light",
    "bg": "#f2f3f9",
    "surface": "#ffffff",
    "card": "#ffffff",
    "card_hover": "#eef0fb",
    "border": "#dfe2f0",
    "input": "#ffffff",
    "text": "#1c1d2c",
    "muted": "#6d6f86",
    "track": "#e3e6f2",
    "brand": "#5a4bd1",
    "brand_hover": "#6c5ce7",
    "danger": "#d43f4c",
}

_current = DARK


def current() -> dict:
    return _current


def is_dark() -> bool:
    return _current is DARK


def set_dark(dark: bool):
    global _current
    _current = DARK if dark else LIGHT


def toggle():
    set_dark(not is_dark())


_QSS = Template("""
QMainWindow, QDialog {
    background: $bg;
}
QWidget {
    color: $text;
    font-family: "Segoe UI", "SF Pro Text", "Ubuntu", sans-serif;
    font-size: 13px;
}
QLabel { background: transparent; }
QLabel#title {
    font-size: 18px;
    font-weight: 700;
}
QLabel#muted { color: $muted; }
QLabel#empty {
    color: $muted;
    font-size: 14px;
}

QPushButton#primary {
    background: $brand;
    color: #ffffff;
    border: none;
    border-radius: 9px;
    padding: 8px 16px;
    font-weight: 600;
}
QPushButton#primary:hover { background: $brand_hover; }
QPushButton#primary:pressed { background: $brand; }

QPushButton#iconbtn {
    background: $surface;
    color: $text;
    border: 1px solid $border;
    border-radius: 9px;
    padding: 7px 11px;
    font-size: 14px;
}
QPushButton#iconbtn:hover { border-color: $brand; }

QTabWidget::pane { border: none; background: transparent; }
QTabBar { background: transparent; }
QTabBar::tab {
    background: transparent;
    color: $muted;
    border: none;
    padding: 9px 16px;
    margin-right: 4px;
    font-weight: 600;
}
QTabBar::tab:selected {
    color: $text;
    border-bottom: 2px solid $brand;
}
QTabBar::tab:hover:!selected { color: $text; }

QScrollArea { border: none; background: transparent; }
QScrollArea > QWidget > QWidget { background: transparent; }
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: $track;
    border-radius: 4px;
    min-height: 28px;
}
QScrollBar::handle:vertical:hover { background: $muted; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }

QLineEdit, QSpinBox, QComboBox {
    background: $input;
    color: $text;
    border: 1px solid $border;
    border-radius: 8px;
    padding: 7px 10px;
    selection-background-color: $brand;
    selection-color: #ffffff;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border-color: $brand; }
QComboBox::drop-down { border: none; width: 24px; }
QComboBox QAbstractItemView {
    background: $surface;
    color: $text;
    border: 1px solid $border;
    border-radius: 8px;
    selection-background-color: $brand;
    selection-color: #ffffff;
    outline: 0;
}
QSpinBox::up-button, QSpinBox::down-button { width: 18px; border: none; }

QMenu {
    background: $surface;
    border: 1px solid $border;
    border-radius: 9px;
    padding: 5px;
}
QMenu::item {
    padding: 7px 20px;
    border-radius: 6px;
}
QMenu::item:selected {
    background: $brand;
    color: #ffffff;
}

QDialog QPushButton {
    background: $surface;
    color: $text;
    border: 1px solid $border;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
}
QDialog QPushButton:hover { border-color: $brand; }
QDialog QPushButton#primary {
    background: $brand;
    color: #ffffff;
    border: none;
    padding: 10px 16px;
}
QDialog QPushButton#primary:hover { background: $brand_hover; }

QMessageBox { background: $surface; }
QToolTip {
    background: $surface;
    color: $text;
    border: 1px solid $border;
    padding: 4px 8px;
}
""")


def stylesheet() -> str:
    return _QSS.substitute(_current)
