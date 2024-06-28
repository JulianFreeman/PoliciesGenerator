# coding: utf8
from PySide6 import QtWidgets, QtCore
from utils import read_template
from gbx_setting import GbxSetting
from gbx_extension import GbxExtension
from gbx_search_engine import GbxSearchEngine


class WgBrowserPage(QtWidgets.QWidget):

    def __init__(self, browser: str, pre_path: str, parent=None):
        super().__init__(parent)
        self.browser = browser
        self.pre_path = pre_path

        self.vly_m = QtWidgets.QVBoxLayout()
        self.setLayout(self.vly_m)
        temp = read_template(browser)

        self.gbx_settings = []
        self.gbx_extensions = []
        self.gbx_search_engines = []

        if "SingleValues" in temp:
            for setting in temp["SingleValues"]:
                gbx_set = GbxSetting(setting, self)
                self.vly_m.addWidget(gbx_set)
                self.gbx_settings.append(gbx_set)

        if "ExtensionSettings" in temp:
            for extension in temp["ExtensionSettings"]:
                gbx_ext = GbxExtension(extension, self)
                self.vly_m.addWidget(gbx_ext)
                self.gbx_extensions.append(gbx_ext)

        if "SearchEngines" in temp:
            self.bgp_search_engines_default = QtWidgets.QButtonGroup(self)
            self.bgp_search_engines_default.setExclusive(True)

            for search_engine in temp["SearchEngines"]:
                gbx_search_engine = GbxSearchEngine(search_engine, self)
                self.vly_m.addWidget(gbx_search_engine)
                self.gbx_search_engines.append(gbx_search_engine)
                self.bgp_search_engines_default.addButton(gbx_search_engine.rbn_default)

    def get_recommended_settings(self):
        recommended_settings = [f"[{self.pre_path}\\Recommended]"]
        for wg_set in self.gbx_settings:
            if wg_set.isChecked() and wg_set.allow_recommend and wg_set.cbx_recommend.isChecked():
                recommended_settings.append(f"\"{wg_set.name}\"=dword:0000000{wg_set.bgp_radios.checkedId()}")
        if len(recommended_settings) == 1:
            return ""
        else:
            return "\n".join(recommended_settings)

    def get_settings(self):
        settings = [f"[{self.pre_path}]"]
        for wg_set in self.gbx_settings:
            if wg_set.isChecked():
                if (wg_set.allow_recommend and not wg_set.cbx_recommend.isChecked()) or (not wg_set.allow_recommend):
                    settings.append(f"\"{wg_set.name}\"=dword:0000000{wg_set.bgp_radios.checkedId()}")
        if len(settings) == 1:
            return ""
        else:
            return "\n".join(settings)

    def get_extensions(self):
        path_head = f"{self.pre_path}\\ExtensionSettings"
        extensions = []
        for wg_ext in self.gbx_extensions:
            if wg_ext.isChecked():
                extensions.append(f"[{path_head}\\{wg_ext.id}]")
                mode = wg_ext.cmbx_modes.currentData(QtCore.Qt.ItemDataRole.UserRole)
                extensions.append(f"\"installation_mode\"=\"{mode}\"")
                extensions.append(f"\"update_url\"=\"{wg_ext.lne_update_url.text()}\"")
        if len(extensions) == 0:
            return ""
        else:
            return "\n".join(extensions)

    def get_search_engines(self):
        # 只生成推荐的
        path_head = f"{self.pre_path}\\Recommended\\ManagedSearchEngines"
        search_engines = []
        i = 1
        for wg_se in self.gbx_search_engines:
            if wg_se.isChecked():
                search_engines.append(f"[{path_head}\\{i}]")
                is_default = "1" if wg_se.rbn_default.isChecked() else "0"
                search_engines.append(f"\"is_default\"=dword:0000000{is_default}")
                search_engines.append(f"\"keyword\"=\"{wg_se.lne_keyword.text()}\"")
                search_engines.append(f"\"name\"=\"{wg_se.lne_name.text()}\"")
                search_engines.append(f"\"search_url\"=\"{wg_se.lne_search_url.text()}\"")
                i += 1
        if len(search_engines) == 0:
            return ""
        else:
            return "\n".join(search_engines)
