# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ["main.py"],
    pathex=["src"],
    binaries=[],
    datas=[],
    hiddenimports=["zxingcpp"],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name="Offline2FA",
    debug=False,
    strip=False,
    upx=False,
    console=False,
)
