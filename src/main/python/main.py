# SPDX-License-Identifier: GPL-2.0-or-later
import ssl
import certifi
import os
import json
from functools import cached_property

if ssl.get_default_verify_paths().cafile is None:
    os.environ["SSL_CERT_FILE"] = certifi.where()

import traceback

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

import sys

from main_window import MainWindow


# http://timlehr.com/python-exception-hooks-with-qt-message-box/
from util import init_logger


def show_exception_box(log_msg):
    if QtWidgets.QApplication.instance() is not None:
        errorbox = QtWidgets.QMessageBox()
        errorbox.setText(log_msg)
        errorbox.exec_()


class UncaughtHook(QtCore.QObject):
    _exception_caught = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super(UncaughtHook, self).__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys._excepthook = sys.excepthook
        sys.excepthook = self.exception_hook

        # connect signal to execute the message box function always on main thread
        self._exception_caught.connect(show_exception_box)

    def exception_hook(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            log_msg = "\n".join(
                [
                    "".join(traceback.format_tb(exc_traceback)),
                    "{0}: {1}".format(exc_type.__name__, exc_value),
                ]
            )

            # trigger message box show
            self._exception_caught.emit(log_msg)
        sys._excepthook(exc_type, exc_value, exc_traceback)


class VialApplicationContext:
    def __init__(self):
        self.bundle_dir = self._get_bundle_dir()
        self.build_settings = self._load_build_settings()

    @cached_property
    def app(self):
        # Override the app definition in order to set WM_CLASS.
        result = QtWidgets.QApplication(sys.argv)
        result.setApplicationName(self.build_settings["app_name"])
        result.setOrganizationName(self.build_settings.get("organization_name", "Vial"))
        result.setOrganizationDomain(
            self.build_settings.get("organization_domain", "vial.today")
        )

        # TODO: Qt sets applicationVersion on non-Linux platforms if the exe/pkg metadata is correctly configured.
        # https://doc.qt.io/qt-5/qcoreapplication.html#applicationVersion-prop
        # Verify it is, and only set manually on Linux.
        # if sys.platform.startswith("linux"):
        result.setApplicationVersion(self.build_settings["version"])
        return result

    def get_resource(self, file_name):
        return self._resource_path(file_name)

    def _load_build_settings(self):
        build_settings = {}
        for file_name in self._settings_file_names():
            with open(file_name, "r", encoding="utf-8") as settings_file:
                build_settings.update(json.load(settings_file))
        return build_settings

    def _get_bundle_dir(self):
        if getattr(sys, "frozen", False):
            return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    def _resource_path(self, file_name):
        if getattr(sys, "frozen", False):
            return os.path.join(self.bundle_dir, "resources", "base", file_name)
        return os.path.join(self.bundle_dir, "main", "resources", "base", file_name)

    def _settings_file_names(self):
        if sys.platform.startswith("linux"):
            platform_settings = "linux"
        elif sys.platform == "darwin":
            platform_settings = "mac"
        elif sys.platform.startswith("win"):
            platform_settings = "windows"
        else:
            platform_settings = None

        file_names = [self._settings_path("base.json")]
        if platform_settings is not None:
            platform_settings_file = self._settings_path(
                "{}.json".format(platform_settings)
            )
            if os.path.exists(platform_settings_file):
                file_names.append(platform_settings_file)
        return file_names

    def _settings_path(self, file_name):
        if getattr(sys, "frozen", False):
            return os.path.join(self.bundle_dir, "resources", "settings", file_name)
        return os.path.join(self.bundle_dir, "build", "settings", file_name)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--linux-recorder":
        from linux_keystroke_recorder import linux_keystroke_recorder

        linux_keystroke_recorder()
    else:
        appctxt = VialApplicationContext()  # 1. Instantiate ApplicationContext
        init_logger()
        qt_exception_hook = UncaughtHook()
        window = MainWindow(appctxt)
        window.show()
        exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()
        sys.exit(exit_code)
