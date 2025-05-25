import os
import json
import platform
import sys
from PyQt5.QtCore import QLocale
from enum import Enum


def is_win11():
    if is_windows():
        if platform.release() >= '10' and int(platform.version().split('.')[2]) >= 22000:
            return True
    return False


def is_win10():
    if is_windows():
        if platform.release() >= '10' and int(platform.version().split('.')[2]) >= 19000:
            return True
    return False


def is_windows():
    return platform.system() == 'Windows'


def resource_path(relative_path):
    """兼容 PyInstaller 打包和开发环境的路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)


rinui_core_path = os.path.abspath(os.path.dirname(__file__))  # RinUI/core 目录

BASE_DIR = os.path.abspath(os.getcwd())
PATH = os.path.join(BASE_DIR, "RinUI/config")
RINUI_PATH = resource_path(os.path.join(rinui_core_path, "../../"))  # 使用 resource_path 处理路径
DEFAULT_CONFIG = {
    "theme": {
        "current_theme": "Auto",
    },
    "win10_feat": {
        "backdrop_light": 0xA6FFFFFF,
        "backdrop_dark": 0xA6000000,
    },
    "theme_color": "#605ed2",
    "backdrop_effect": "mica" if is_win11() else "acrylic" if is_win10() else "none",
}


class Theme(Enum):
    Auto = "Auto"
    Dark = "Dark"
    Light = "Light"


class BackdropEffect(Enum):
    None_ = "none"
    Acrylic = "acrylic"
    Mica = "mica"
    Tabbed = "tabbed"


class ConfigManager:
    def __init__(self, path, filename):
        """
        Json Config Manager
        :param path: json config file path
        :param filename: json config file name (eg: rin_ui.json)
        """
        self.path = path
        self.filename = filename
        self.config = {}
        self.full_path = os.path.join(self.path, self.filename)

    def load_config(self, default_config):
        if default_config is None:
            print('Warning: "default_config" is None, use empty config instead.')
            default_config = {}
        # 如果文件存在，加载配置
        if os.path.exists(self.full_path):
            with open(self.full_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = default_config  # 如果文件不存在，使用默认配置
            self.save_config()

    def update_config(self):  # 更新配置
        try:
            with open(self.full_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f'Error: {e}')
            self.config = {}

    def upload_config(self, key=str or list, value=None):
        if type(key) is str:
            self.config[key] = value
        elif type(key) is list:
            for k in key:
                self.config[k] = value
        else:
            raise TypeError('key must be str or list')
        self.save_config()

    def save_config(self):
        try:
            # 确保配置文件目录存在
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            with open(self.full_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'Error: {e}')

    def __getitem__(self, key):
        return self.config.get(key)

    def __setitem__(self, key, value):
        self.config[key] = value
        self.save_config()

    def __repr__(self):
        return json.dumps(self.config, ensure_ascii=False, indent=4)


RinConfig = ConfigManager(path=PATH, filename='rin_ui.json')
RinConfig.load_config(DEFAULT_CONFIG)  # 加载配置
