# coding: utf8
from PySide6 import QtWidgets


class GbxSearchEngine(QtWidgets.QGroupBox):

    def __init__(self, search_engines_info: dict, parent=None):
        super().__init__(parent)
        self.vly_m = QtWidgets.QVBoxLayout()
        self.setLayout(self.vly_m)
        self.setTitle(f'搜索引擎：{search_engines_info["number"]}')
        self.setCheckable(True)
        self.setChecked(search_engines_info["enabled"])

        self.gly_info = QtWidgets.QGridLayout()
        self.vly_m.addLayout(self.gly_info)

        self.lb_name = QtWidgets.QLabel("名称：", self)
        self.lne_name = QtWidgets.QLineEdit(search_engines_info["name"], self)
        self.lb_keyword = QtWidgets.QLabel("关键词：", self)
        self.lne_keyword = QtWidgets.QLineEdit(search_engines_info["keyword"], self)
        self.lb_search_url = QtWidgets.QLabel("搜索链接：", self)
        self.lne_search_url = QtWidgets.QLineEdit(search_engines_info["search_url"], self)
        self.lne_search_url.setCursorPosition(0)
        self.gly_info.addWidget(self.lb_name, 0, 0)
        self.gly_info.addWidget(self.lne_name, 0, 1)
        self.gly_info.addWidget(self.lb_keyword, 1, 0)
        self.gly_info.addWidget(self.lne_keyword, 1, 1)
        self.gly_info.addWidget(self.lb_search_url, 2, 0)
        self.gly_info.addWidget(self.lne_search_url, 2, 1)

        self.rbn_default = QtWidgets.QRadioButton("设为默认", self)
        self.vly_m.addWidget(self.rbn_default)
        self.rbn_default.setChecked(search_engines_info["is_default"])
