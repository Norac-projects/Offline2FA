import hashlib

from PySide6.QtGui import QColor


def accent_for(name: str, dark: bool) -> QColor:
    digest = hashlib.md5(name.strip().lower().encode("utf-8")).hexdigest()
    hue = int(digest[:8], 16) % 360
    if dark:
        return QColor.fromHsl(hue, 170, 160)
    return QColor.fromHsl(hue, 165, 115)


def account_accent(account, dark: bool) -> QColor:
    if account.color:
        color = QColor(account.color)
        if color.isValid():
            return color
    return accent_for(account.display_name, dark)
