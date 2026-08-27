import sys

from PySide6.QtWidgets import QApplication

from .storage import Store
from .ui import theme
from .ui.window import MainWindow


def run() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Offline 2FA")
    app.setOrganizationName("Norac Projects")

    store = Store()
    theme.set_dark(store.theme != "light")
    app.setStyleSheet(theme.stylesheet())

    window = MainWindow(store, app)
    window.show()
    return app.exec()
