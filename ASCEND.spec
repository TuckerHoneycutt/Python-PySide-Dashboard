# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['MainGui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ASCEND',
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
    icon=['/Users/tuckerhoneycutt/projects/python/Work/n1uTw9NYigfpF0A2dRwLnplEskWfgjmT.icns'],
)
app = BUNDLE(
    exe,
    name='ASCEND.app',
    icon='/Users/tuckerhoneycutt/projects/python/Work/n1uTw9NYigfpF0A2dRwLnplEskWfgjmT.icns',
    bundle_identifier=None,
)
