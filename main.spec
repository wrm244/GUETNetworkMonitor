# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['network_utils.py', 'authentication_utils.py', 'encryption_utils.py','login_window.py','monitor_thread.py','monitor_window.py','utils.py'],
    binaries=[],
    datas=[],
    hiddenimports=['encryption_utils', 'network_utils', 'authentication_utils','login_window','monitor_thread','monitor_window','utils'],
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
