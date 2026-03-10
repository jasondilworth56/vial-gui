#!/bin/bash

set -e

cd /vial-gui
python3 -m venv docker_venv
. docker_venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pyinstaller misc/Vial.spec

cp src/main/icons/linux/1024.png dist/Vial/Vial.png
cp misc/Vial.desktop dist/Vial/
cp misc/AppRun dist/Vial/
chmod +x dist/Vial/AppRun

deactivate
/appimagetool-x86_64.AppImage dist/Vial
mv Vial-x86_64.AppImage /output/Vial-x86_64.AppImage
