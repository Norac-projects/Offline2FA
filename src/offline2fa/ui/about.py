from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget

from .. import __version__

ABOUT_TEXT = f"""
<h2 style="margin-bottom:2px;">Offline 2FA</h2>
<p style="margin-top:0;">Version {__version__} &middot; a Norac Project</p>

<p>Offline 2FA is a small, fully offline authenticator for your desktop. Paste a
2FA secret once and it gives you the code &mdash; the same six digits your
phone app would show &mdash; refreshing every 30 seconds.</p>

<p>No websites, no accounts, no cloud. Unlike the "paste your secret here"
sites floating around the internet, nothing ever leaves your computer. Your
secrets sit in a plain file in your own user folder and stay there.</p>

<p>Good to know:</p>
<ul>
<li>Click any card to copy its code.</li>
<li>Right-click a card to remove it.</li>
<li>Just paste the secret key most of the time. If a service gives you a full
setup link or QR code instead, use those &mdash; Offline 2FA reads the details out
of them automatically, including the rare services that use different settings.</li>
</ul>

<p>Since it's your only copy, back up your secrets somewhere safe.</p>

<p>Contact us:</p>
<p>Telegram : @NoracProjects</p>
<p>Email : Norac-Projects@Proton.me

<p>Released under the MIT license.</p>
"""


class AboutTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QLabel(ABOUT_TEXT)
        content.setWordWrap(True)
        content.setTextFormat(Qt.RichText)
        content.setAlignment(Qt.AlignTop)
        content.setContentsMargins(18, 10, 18, 18)
        content.setOpenExternalLinks(True)

        scroll.setWidget(content)
        layout.addWidget(scroll)
