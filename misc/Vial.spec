# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import sys


ROOT = Path(SPECPATH).resolve().parent
WINDOWS_ICON = str(ROOT / "src/main/icons/Icon.ico")

if sys.platform.startswith("win"):
    EXE_ICON = [WINDOWS_ICON]
else:
    EXE_ICON = None

if sys.platform == "darwin":
    BUNDLE_ICON = None
else:
    BUNDLE_ICON = None

a = Analysis(
    [str(ROOT / "src/main/python/main.py")],
    pathex=[str(ROOT / "src/main/python")],
    binaries=[],
    datas=[
        (str(ROOT / "src/main/resources/base/qmk_settings.json"), "resources/base"),
        (str(ROOT / "src/build/settings/base.json"), "resources/settings"),
        (str(ROOT / "src/build/settings/linux.json"), "resources/settings"),
        (str(ROOT / "src/build/settings/mac.json"), "resources/settings"),
    ],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name="Vial",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    contents_directory=".",
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=EXE_ICON,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Vial",
)
app = BUNDLE(
    coll,
    name="Vial.app",
    icon=BUNDLE_ICON,
    bundle_identifier=None,
)
