# coding: utf8
from PySide6 import QtWidgets, QtCore, QtGui


class GbxSetting(QtWidgets.QGroupBox):

    def __init__(self, setting_info: dict, parent=None):
        super().__init__(parent)
        self.vly_m = QtWidgets.QVBoxLayout()
        self.setLayout(self.vly_m)
        self.setTitle(setting_info["display_name"])
        self.setCheckable(True)
        self.setChecked(setting_info["enabled"])

        self.bgp_radios = QtWidgets.QButtonGroup(self)
        self.bgp_radios.setExclusive(True)

        for i, name in setting_info["values"].items():
            value = int(i)
            rbn_1 = QtWidgets.QRadioButton(name, self)
            self.bgp_radios.addButton(rbn_1, id=value)
            self.vly_m.addWidget(rbn_1)
            if setting_info["default_value"] == value:
                rbn_1.setChecked(True)

        self.allow_recommend = setting_info["allow_recommend"]
        if self.allow_recommend:
            self.cbx_recommend = QtWidgets.QCheckBox("设置为推荐", self)
            self.vly_m.addWidget(self.cbx_recommend)
            self.cbx_recommend.setChecked(True)
            self.cbx_recommend.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)

        self.name = setting_info["name"]
