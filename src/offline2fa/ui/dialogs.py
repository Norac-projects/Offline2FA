from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog, QFileDialog, QLabel, QLineEdit,
                               QMessageBox, QPushButton, QVBoxLayout)

from .. import qr, uri
from ..storage import Account


class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add account")
        self.setModal(True)
        self.setMinimumWidth(420)
        self.account: Account | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(10)

        heading = QLabel("Paste your 2FA secret")
        heading.setObjectName("title")
        layout.addWidget(heading)

        hint = QLabel("Paste the secret key or the setup link your service gave you. "
                      "Offline 2FA figures out the rest.")
        hint.setObjectName("muted")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        self.secret_edit = QLineEdit()
        self.secret_edit.setPlaceholderText("secret key  or  otpauth://...")
        self.secret_edit.returnPressed.connect(self._try_accept)
        layout.addWidget(self.secret_edit)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Name it (optional) \u2014 e.g. GitHub")
        self.name_edit.returnPressed.connect(self._try_accept)
        layout.addWidget(self.name_edit)

        qr_btn = QPushButton("Or import a QR code image\u2026")
        qr_btn.setCursor(Qt.PointingHandCursor)
        qr_btn.clicked.connect(self._pick_image)
        layout.addWidget(qr_btn)

        layout.addSpacing(4)
        add_btn = QPushButton("Add")
        add_btn.setObjectName("primary")
        add_btn.setDefault(True)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self._try_accept)
        layout.addWidget(add_btn)

        self.secret_edit.setFocus()

    def _pick_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose QR image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp *.gif)")
        if not path:
            return
        try:
            self.account = uri.parse(qr.read_image(path))
        except Exception as exc:
            QMessageBox.warning(self, "Couldn't read that image", str(exc))
            return
        self.accept()

    def _try_accept(self):
        try:
            self.account = uri.smart_build(self.secret_edit.text(),
                                           self.name_edit.text())
        except Exception:
            QMessageBox.warning(
                self, "That doesn't look right",
                "Double-check the secret \u2014 it should be the key your service "
                "gave you, or a link that starts with otpauth://")
            return
        self.accept()
