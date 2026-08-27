import time

from PySide6.QtCore import Qt, QRectF, QTimer
from PySide6.QtGui import QColor, QGuiApplication, QPainter, QPainterPath
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QMenu,
                               QPushButton, QVBoxLayout)

from .. import otp
from ..colors import account_accent
from . import theme
from .widgets import CountdownRing, code_font


def format_code(code: str) -> str:
    half = len(code) // 2
    return f"{code[:half]} {code[half:]}"


class AccountCard(QFrame):
    def __init__(self, account, on_delete, on_save, parent=None):
        super().__init__(parent)
        self.account = account
        self.on_delete = on_delete
        self.on_save = on_save
        self._hover = False
        self._code = ""
        self._totp_counter = -1

        self.setFixedHeight(94)
        self.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 14, 18, 14)
        layout.setSpacing(14)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        self.issuer_label = QLabel(account.display_name)
        self.name_label = QLabel(account.name if account.issuer else "")
        self.name_label.setVisible(bool(self.name_label.text()))
        text_col.addStretch()
        text_col.addWidget(self.issuer_label)
        text_col.addWidget(self.name_label)
        text_col.addStretch()
        layout.addLayout(text_col, 1)

        self.code_label = QLabel()
        self.code_label.setFont(code_font(21))
        layout.addWidget(self.code_label)

        self.accent = account_accent(account, theme.is_dark())

        if account.kind == "totp":
            self.ring = CountdownRing(self.accent)
            layout.addWidget(self.ring)
        else:
            self.advance_btn = QPushButton("\u21bb")
            self.advance_btn.setFixedSize(52, 52)
            self.advance_btn.setCursor(Qt.PointingHandCursor)
            self.advance_btn.setToolTip("Next code")
            self.advance_btn.clicked.connect(self._advance)
            layout.addWidget(self.advance_btn)

        self.toast = QLabel("Copied", self)
        self.toast.hide()

        self.restyle()
        self.refresh_code()

    def restyle(self):
        palette = theme.current()
        self.accent = account_accent(self.account, theme.is_dark())
        self.issuer_label.setStyleSheet(
            f"color: {palette['text']}; font-size: 14px; font-weight: 600;")
        self.name_label.setStyleSheet(f"color: {palette['muted']}; font-size: 12px;")
        self.code_label.setStyleSheet(f"color: {self.accent.name()};")
        self.toast.setStyleSheet(
            f"background: {self.accent.name()}; color: #ffffff;"
            "border-radius: 11px; padding: 4px 12px; font-weight: 600;")
        if self.account.kind == "totp":
            self.ring.accent = self.accent
            self.ring.update()
        else:
            self.advance_btn.setStyleSheet(
                f"QPushButton {{ background: transparent; color: {self.accent.name()};"
                f"border: 3px solid {palette['track']}; border-radius: 26px;"
                "font-size: 20px; font-weight: 700; }"
                f"QPushButton:hover {{ border-color: {self.accent.name()}; }}")
        self.update()

    def tick(self):
        if self.account.kind != "totp":
            return
        now = time.time()
        counter = int(now // self.account.period)
        if counter != self._totp_counter:
            self._totp_counter = counter
            self.refresh_code()
        remaining = self.account.period - (now % self.account.period)
        self.ring.set_state(remaining / self.account.period, int(remaining) + 1)

    def refresh_code(self):
        try:
            if self.account.kind == "totp":
                self._code = otp.totp(self.account.secret, self.account.digits,
                                      self.account.algorithm, self.account.period)
            else:
                self._code = otp.hotp(self.account.secret, self.account.counter,
                                      self.account.digits, self.account.algorithm)
            self.code_label.setText(format_code(self._code))
        except Exception:
            self._code = ""
            self.code_label.setText("invalid")

    def _advance(self):
        self.account.counter += 1
        self.on_save()
        self.refresh_code()

    def copy_code(self):
        if not self._code:
            return
        QGuiApplication.clipboard().setText(self._code)
        self.toast.adjustSize()
        self.toast.move((self.width() - self.toast.width()) // 2,
                        (self.height() - self.toast.height()) // 2)
        self.toast.show()
        self.toast.raise_()
        QTimer.singleShot(900, self.toast.hide)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.rect().contains(event.position().toPoint()):
            self.copy_code()
        super().mouseReleaseEvent(event)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        copy_action = menu.addAction("Copy code")
        delete_action = menu.addAction("Delete account")
        chosen = menu.exec(event.globalPos())
        if chosen == copy_action:
            self.copy_code()
        elif chosen == delete_action:
            self.on_delete(self.account)

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        palette = theme.current()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, 14, 14)
        painter.fillPath(path, QColor(palette["card_hover" if self._hover else "card"]))
        painter.setPen(QColor(palette["border"]))
        painter.drawPath(path)

        bar = QPainterPath()
        bar.addRoundedRect(QRectF(12, rect.height() / 2 - 15, 4, 30), 2, 2)
        painter.fillPath(bar, self.accent)
        painter.end()
