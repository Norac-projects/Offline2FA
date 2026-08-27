# Offline 2FA 🔐

**Your 2FA codes, on your desktop, fully offline. Paste your secret, get your code. That's the whole app.**

A Norac Project.

---

## Why this exists

Here's a scene you've lived through. A website wants your 2FA code, your phone is charging in another room, and you find yourself googling "2fa code generator online" and pasting your secret key into some random site like 2fa.live.

Stop for a second. That secret key **is** your second factor. Typing it into a website you know nothing about hands the keys to a stranger and quietly undoes the entire reason you turned on 2FA.

Offline 2FA does the same job, minus the stranger. Paste your secret once, get a fresh code every 30 seconds, forever. No website, no server, no account, no internet. It runs on your machine and stays there.

## Dead simple on purpose

Other authenticator apps bury you in dropdowns — algorithm, digits, period, counter type. Offline 2FA doesn't ask any of that. You paste the secret, you get the code. Done.

The clever bit: almost every service on earth uses the same standard settings, so there's nothing to configure. And for the rare service that's different, it hands you a setup **link** or **QR code** that already contains its settings — Offline 2FA reads those automatically. Either way, you never touch a single option.

## What you get

- ⚡ **One-box setup** — paste a secret key or an `otpauth://` link, hit Add, you're done
- 📷 **QR import** — got a QR code screenshot instead? Drop the image in and it reads it
- 🔄 **Auto-refresh** — codes roll over every 30 seconds, smooth, no flicker, no lag
- 📋 **Click to copy** — tap any card, the code's on your clipboard
- 🎨 **Not another gray utility** — each account gets its own color, a live countdown ring, and clean type. Dark mode by default, light mode one click away
- 🔒 **Truly offline** — there is no network code in this project. Nothing to leak, nothing to trust
- 🧠 **Handles the weird ones** — 8-digit codes, alternate hash algorithms, odd time steps: all supported automatically when a service needs them, invisible when it doesn't

## Getting started

```bash
git clone https://github.com/Norac-projects/Offline2FA.git
cd Offline2FA
pip install -r requirements.txt
python main.py
```

One entry point, one command. Requires **Python 3.13**.

Never touched Python before? Follow [THE_POTATO_PROTOCOL.md](THE_POTATO_PROTOCOL.md) — every step spelled out, zero assumptions.

## Want a single .exe?

Build a standalone Windows executable that runs anywhere with nothing installed:

```bash
pyinstaller Offline2FA.spec
```

Your file lands at `dist/Offline2FA.exe`. One file. Double-click. No Python, no installer, no dependencies on the target machine.

## Where your data lives

Accounts are saved in a plain JSON file in your own user folder:

| OS      | Location                                 |
| ------- | ---------------------------------------- |
| Windows | `%APPDATA%\Offline2FA\accounts.json`        |
| macOS   | `~/Library/Application Support/Offline2FA/` |
| Linux   | `~/.config/Offline2FA/`                     |

It never leaves your machine unless you move it. It's your only copy, so back it up somewhere safe.

## Languages used

| Language | Share |
| -------- | ----- |
| Python   | 100%  |

GitHub will report this repo as **100% Python** — the whole thing, UI included, is Python 3.13.

## Built with

| Library         | Used for                | License                              |
| --------------- | ----------------------- | ------------------------------------ |
| **PySide6 (Qt)**| the interface           | LGPL-3.0                             |
| **zxing-cpp**   | reading QR code images  | Apache-2.0                          |
| **Pillow**      | opening image files     | MIT-CMU (HPND)                      |
| **PyInstaller** | building the .exe       | GPL-2.0 w/ bootloader exception     |

All four are safe to use and share in an open-source project. PySide6 is dynamically linked (LGPL-compliant), zxing-cpp and Pillow are permissive, and PyInstaller is only a build tool — it's never bundled into the app, and its bootloader exception explicitly permits distributing the resulting executables under any license.

The 2FA code generation itself uses **only the Python standard library** (`hmac`, `hashlib`, `struct`, `base64`) — no crypto dependency to trust or audit. It follows the published standards **RFC 6238** (time-based) and **RFC 4226** (counter-based), and the implementation is verified against the official test vectors in those RFCs.

## Project layout

```
Offline2FA/
├── main.py              entry point — run this
├── Offline2FA.spec         PyInstaller build recipe
├── requirements.txt
└── src/offline2fa/
    ├── otp.py           the code generator (RFC 6238 / 4226)
    ├── uri.py           reads otpauth:// links and raw secrets
    ├── qr.py            QR image import
    ├── storage.py       local JSON persistence
    ├── colors.py        per-account accent colors
    └── ui/              window, cards, add dialog, About, theming
```

## License

MIT — see [LICENSE](LICENSE). Use it, fork it, ship it.

---

*Part of Norac Projects.*
