FROM ubuntu:22.04

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3 python3-venv python3-pip libusb-1.0-0-dev libudev-dev build-essential desktop-file-utils wget unzip zlib1g-dev liblzma-dev libssl-dev git imagemagick file libfuse2

RUN wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage -O /appimagetool-x86_64.AppImage && \
    chmod +x /appimagetool-x86_64.AppImage

COPY . /vial-gui
