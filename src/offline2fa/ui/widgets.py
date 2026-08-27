from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget

from . import theme


def code_font(size: int) -> QFont:
    font = QFont()
    font.setFamilies(["Cascadia Mono", "Consolas", "SF Mono", "Menlo", "DejaVu Sans Mono"])
    font.setPointSize(size)
    font.setBold(True)
    return font


class CountdownRing(QWidget):
    def __init__(self, accent: QColor, parent=None):
        super().__init__(parent)
        self.setFixedSize(52, 52)
        self.accent = accent
        self._fraction = 1.0
        self._seconds = 0

    def set_state(self, fraction: float, seconds: int):
        if abs(fraction - self._fraction) < 0.002 and seconds == self._seconds:
            return
        self._fraction = fraction
        self._seconds = seconds
        self.update()

    def paintEvent(self, event):
        palette = theme.current()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(4, 4, -4, -4)
        pen = QPen(QColor(palette["track"]), 4)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawEllipse(rect)

        pen.setColor(self.accent)
        painter.setPen(pen)
        painter.drawArc(rect, 90 * 16, int(-360 * 16 * self._fraction))

        painter.setPen(QColor(palette["text"]))
        font = self.font()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, str(self._seconds))
        painter.end()
