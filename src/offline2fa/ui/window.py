from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QMainWindow, QMessageBox,
                               QPushButton, QScrollArea, QTabWidget,
                               QVBoxLayout, QWidget)

from . import theme
from .about import AboutTab
from .cards import AccountCard
from .dialogs import AddAccountDialog


class MainWindow(QMainWindow):
    def __init__(self, store, app):
        super().__init__()
        self.store = store
        self.app = app
        self.cards: list[AccountCard] = []

        self.setWindowTitle("Offline 2FA")
        self.resize(430, 660)
        self.setMinimumSize(380, 480)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 14, 16, 14)
        root.setSpacing(10)

        header = QHBoxLayout()
        title = QLabel("Offline 2FA")
        title.setObjectName("title")
        header.addWidget(title)
        header.addStretch()

        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("iconbtn")
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.setToolTip("Switch theme")
        self.theme_btn.clicked.connect(self.toggle_theme)
        header.addWidget(self.theme_btn)

        add_btn = QPushButton("+ Add")
        add_btn.setObjectName("primary")
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_account)
        header.addWidget(add_btn)
        root.addLayout(header)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_accounts_page(), "Accounts")
        self.tabs.addTab(AboutTab(), "About")
        root.addWidget(self.tabs)

        self._update_theme_button()
        self.rebuild()

        self.timer = QTimer(self)
        self.timer.setInterval(80)
        self.timer.timeout.connect(self._tick)
        self.timer.start()

    def _build_accounts_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 8, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        inner = QWidget()
        self.card_layout = QVBoxLayout(inner)
        self.card_layout.setContentsMargins(2, 2, 6, 2)
        self.card_layout.setSpacing(10)

        self.empty_label = QLabel("Nothing here yet.\nHit  + Add  to bring in your first account.")
        self.empty_label.setObjectName("empty")
        self.empty_label.setAlignment(Qt.AlignCenter)

        self.card_layout.addWidget(self.empty_label)
        self.card_layout.addStretch()

        scroll.setWidget(inner)
        layout.addWidget(scroll)
        return page

    def rebuild(self):
        for card in self.cards:
            self.card_layout.removeWidget(card)
            card.deleteLater()
        self.cards = []

        for index, account in enumerate(self.store.accounts):
            card = AccountCard(account, self.delete_account, self.store.save)
            self.card_layout.insertWidget(1 + index, card)
            self.cards.append(card)

        self.empty_label.setVisible(not self.cards)

    def _tick(self):
        for card in self.cards:
            card.tick()

    def add_account(self):
        dialog = AddAccountDialog(self)
        if dialog.exec() and dialog.account:
            self.store.add(dialog.account)
            self.rebuild()

    def delete_account(self, account):
        answer = QMessageBox.question(
            self, "Delete account",
            f"Remove {account.display_name}?\n\n"
            "Make sure you have another way to sign in first.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.Yes:
            self.store.remove(account.id)
            self.rebuild()

    def toggle_theme(self):
        theme.toggle()
        self.store.theme = theme.current()["name"]
        self.store.save()
        self.app.setStyleSheet(theme.stylesheet())
        self._update_theme_button()
        for card in self.cards:
            card.restyle()

    def _update_theme_button(self):
        self.theme_btn.setText("\u2600" if theme.is_dark() else "\u263e")
