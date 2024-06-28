# coding: utf8
from PySide6 import QtCore, QtWidgets


class ExtensionModesListModel(QtCore.QAbstractListModel):

    def __init__(self, modes_info: dict, parent=None):
        super().__init__(parent)
        self.modes = []
        self.display_modes = []
        for k, v in modes_info.items():
            self.modes.append(k)
            self.display_modes.append(v)

    def rowCount(self, parent: QtCore.QModelIndex = ...):
        return len(self.modes)

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        row = index.row()

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.display_modes[row]
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return self.modes[row]


class GbxExtension(QtWidgets.QGroupBox):

    def __init__(self, extension_info: dict, parent=None):
        super().__init__(parent)
        self.vly_m = QtWidgets.QVBoxLayout()
        self.setLayout(self.vly_m)
        self.setTitle(extension_info["name"])
        self.setCheckable(True)
        self.setChecked(extension_info["enabled"])

        self.lb_desc = QtWidgets.QLabel(extension_info["description"], self)
        self.vly_m.addWidget(self.lb_desc)

        self.lb_modes = QtWidgets.QLabel("安装模式：", self)
        self.cmbx_modes = QtWidgets.QComboBox(self)
        modes_model = ExtensionModesListModel(extension_info["modes"], self)
        self.cmbx_modes.setModel(modes_model)
        self.cmbx_modes.setCurrentIndex(modes_model.modes.index(extension_info["default_mode"]))
        self.lb_update_url = QtWidgets.QLabel("更新链接：", self)
        self.lne_update_url = QtWidgets.QLineEdit(extension_info["update_url"], self)

        self.hly_modes = QtWidgets.QHBoxLayout()
        self.vly_m.addLayout(self.hly_modes)
        self.hly_modes.addWidget(self.lb_modes)
        self.hly_modes.addWidget(self.cmbx_modes)
        self.hly_modes.addStretch(1)
        self.hly_update_url = QtWidgets.QHBoxLayout()
        self.vly_m.addLayout(self.hly_update_url)
        self.hly_update_url.addWidget(self.lb_update_url)
        self.hly_update_url.addWidget(self.lne_update_url)

        self.id = extension_info["id"]
