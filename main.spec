# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ui/main.py'],
    pathex=['./network_utils.py', './authentication_utils.py', './encryption_utils.py','ui/login_window.py','ui/monitor_thread.py','ui/monitor_window.py','ui/utils.py'],
    binaries=[],
    datas=[],
    hiddenimports=['./encryption_utils', './network_utils', './authentication_utils','ui/login_window','ui/monitor_thread','ui/monitor_window','ui/utils'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='桂电校园网监视',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
