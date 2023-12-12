# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['D:/Projects/Attendance/main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/Projects/Attendance/face_recognition_models', 'face_recognition_models/'), ('D:/Projects/Attendance/fa/Lib/site-packages/mediapipe/modules', 'mediapipe/modules/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Attendance System',
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
    icon=['D:\\Projects\\Attendance\\GettyImages-1198430065.ico'],
)
