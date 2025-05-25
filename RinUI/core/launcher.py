import os
import sys

from PyQt5.QtCore import QCoreApplication, QUrl, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

from .theme import ThemeManager
from .config import BackdropEffect, is_windows, Theme, RINUI_PATH, RinConfig


class RinUIWindow:
    def __init__(self, qml_path: str):
        """
        Create an application window with RinUI.
        :param qml_path: str, QML file path (eg = "path/to/main.qml")
        """
        super().__init__()
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True
        print("✨ RinUIWindow Initializing")

        # 退出清理
        app_instance = QCoreApplication.instance()
        if not app_instance:
            raise RuntimeError("QApplication must be created before RinUIWindow.")

        self.engine = QQmlApplicationEngine()
        self.theme_manager = ThemeManager()
        self.qml_path = qml_path
        self.autoSetWindowsEffect = True

        app_instance.aboutToQuit.connect(self.theme_manager.clean_up)
        self._setup_application()
        self.print_startup_info()

    def _setup_application(self) -> None:
        """Setup"""
        # RInUI 模块
        print(f"UI Module Path: {RINUI_PATH}")

        if os.path.exists(RINUI_PATH):
            self.engine.addImportPath(RINUI_PATH)
        else:
            raise FileNotFoundError(f"Cannot find RinUI module: {RINUI_PATH}")

        # 主题管理器
        self.engine.rootContext().setContextProperty("ThemeManager", self.theme_manager)
        try:
            self.engine.load(self.qml_path)
        except Exception as e:
            print(f"Cannot Load QML file: {e}")

        if not self.engine.rootObjects():
            raise RuntimeError(f"Error loading QML file: {self.qml_path}")

        # 窗口设置
        self.root_window = self.engine.rootObjects()[0]

        self.theme_manager.set_window(self.root_window)
        self._apply_windows_effects() if self.autoSetWindowsEffect else None

    def setIcon(self, path: str) -> None:
        """
        Sets the icon for the application.
        :param path: str, icon file path (eg = "path/to/icon.png")
        :return:
        """
        app_instance = QApplication.instance()
        if app_instance:
            app_instance.setWindowIcon(QIcon(path))  # 设置应用程序图标
            self.root_window.setProperty('icon', QUrl.fromLocalFile(path))
        else:
            raise RuntimeError("Cannot set icon before QApplication is created.")

    def _apply_windows_effects(self) -> None:
        """
        Apply Windows effects to the window.
        :return:
        """
        if sys.platform == "win32":
            self.theme_manager.apply_backdrop_effect(self.theme_manager.get_backdrop_effect())
            self.theme_manager.apply_window_effects()

    # func名称遵循 Qt 命名规范
    def setBackdropEffect(self, effect: BackdropEffect) -> None:
        """
        Sets the backdrop effect for the window. (Only available on Windows)
        :param effect: BackdropEffect, type of backdrop effect（Acrylic, Mica, Tabbed, None_）
        :return:
        """
        if not is_windows() and effect != BackdropEffect.None_:
            raise OSError("Only can set backdrop effect on Windows platform.")
        self.theme_manager.apply_backdrop_effect(effect.value)

    def setTheme(self, theme: Theme) -> None:
        """
        Sets the theme for the window.
        :param theme: Theme, type of theme（Auto, Dark, Light）
        :return:
        """
        self.theme_manager.toggle_theme(theme.value)

    def __getattr__(self, name) -> QObject:
        """获取 QML 窗口属性"""
        try:
            root = object.__getattribute__(self, "root_window")
            return getattr(root, name)
        except AttributeError:
            raise AttributeError(f"\"RinUIWindow\" object has no attribute '{name}'")

    def print_startup_info(self) -> None:
        border = "=" * 40
        print(f"\n{border}")
        print("✨ RinUIWindow Loaded Successfully!")
        print(f"QML File Path: {self.qml_path}")
        print(f"Current Theme: {self.theme_manager.current_theme}")
        print(f"Backdrop Effect: {self.theme_manager.get_backdrop_effect()}")
        print(f"OS: {sys.platform}")
        print(border + "\n")


if __name__ == "__main__":
    # 新用法，应该更规范了捏
    app = QApplication(sys.argv)
    example = RinUIWindow("../../examples/gallery.qml")
    sys.exit(app.exec())
