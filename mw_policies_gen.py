# coding: utf8
import sys
from PySide6 import QtWidgets, QtCore, QtGui

from wg_browser_page import WgBrowserPage


class BrowsersListModel(QtCore.QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.browsers = ["Chrome", "Edge", "Brave"]
        self.browser_vars = ["chrome", "edge", "brave"]
        self.icons = [
            QtGui.QIcon(":/images/browsers/chrome_32.png"),
            QtGui.QIcon(":/images/browsers/edge_32.png"),
            QtGui.QIcon(":/images/browsers/brave_32.png"),
        ]

    def rowCount(self, parent: QtCore.QModelIndex = ...):
        return len(self.browsers)

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        row = index.row()

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.browsers[row]
        if role == QtCore.Qt.ItemDataRole.DecorationRole:
            return self.icons[row]
        if role == QtCore.Qt.ItemDataRole.UserRole:
            return self.browser_vars[row]


class AppStyleListModel(QtCore.QAbstractListModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        if sys.platform == "win32":
            self.styles = ["fusion", "windowsvista", "windows11", "windows"]
        elif sys.platform == "darwin":
            self.styles = ["fusion", "macos", "windows"]
        else:
            self.styles = []

    def rowCount(self, parent: QtCore.QModelIndex = ...):
        return len(self.styles)

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        row = index.row()

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.styles[row]


class UiMwPoliciesGen(object):

    def __init__(self, window: QtWidgets.QWidget):
        self.vly_m = QtWidgets.QVBoxLayout()
        window.setLayout(self.vly_m)

        self.hly_top = QtWidgets.QHBoxLayout()
        self.vly_m.addLayout(self.hly_top)

        self.cmbx_browsers = QtWidgets.QComboBox(window)
        self.hly_top.addWidget(self.cmbx_browsers)

        self.vln_1 = QtWidgets.QFrame(window)
        self.vln_1.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.vln_1.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.hly_top.addWidget(self.vln_1)

        self.pbn_export = QtWidgets.QPushButton("导出", window)
        self.hly_top.addWidget(self.pbn_export)
        self.pbn_about = QtWidgets.QPushButton("关于", window)
        self.hly_top.addWidget(self.pbn_about)

        self.hly_top.addStretch(1)
        self.lb_styles = QtWidgets.QLabel("主题：", window)
        self.hly_top.addWidget(self.lb_styles)
        self.cmbx_styles = QtWidgets.QComboBox(window)
        self.hly_top.addWidget(self.cmbx_styles)

        self.sw_policies = QtWidgets.QStackedWidget(window)
        self.vly_m.addWidget(self.sw_policies)

        # ============== Stacks ===========================

        self.sa_chrome_page = QtWidgets.QScrollArea(self.sw_policies)
        self.sa_edge_page = QtWidgets.QScrollArea(self.sw_policies)
        self.sa_brave_page = QtWidgets.QScrollArea(self.sw_policies)

        self.sw_policies.addWidget(self.sa_chrome_page)
        self.sw_policies.addWidget(self.sa_edge_page)
        self.sw_policies.addWidget(self.sa_brave_page)

        # =============== Page ======================

        self.wg_chrome_page = WgBrowserPage("chrome",
                                            "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Google\\Chrome",
                                            self.sa_chrome_page)
        self.sa_chrome_page.setWidget(self.wg_chrome_page)
        self.sa_chrome_page.setWidgetResizable(True)

        self.wg_edge_page = WgBrowserPage("edge",
                                          "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Edge",
                                          self.sa_edge_page)
        self.sa_edge_page.setWidget(self.wg_edge_page)
        self.sa_edge_page.setWidgetResizable(True)

        self.wg_brave_page = WgBrowserPage("brave",
                                           "HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\BraveSoftware\\Brave",
                                           self.sa_brave_page)
        self.sa_brave_page.setWidget(self.wg_brave_page)
        self.sa_brave_page.setWidgetResizable(True)


class MwPoliciesGen(QtWidgets.QWidget):

    def __init__(self, version: tuple[int, ...], parent=None):
        super().__init__(parent)
        self.ui = UiMwPoliciesGen(self)
        self.setWindowTitle("浏览器策略生成器")
        self.setWindowIcon(QtGui.QIcon(":/images/policies_gen_128.png"))

        self.version = version

        self.ui.cmbx_browsers.setModel(BrowsersListModel(self))
        self.ui.cmbx_browsers.currentIndexChanged.connect(self.ui.sw_policies.setCurrentIndex)

        self.ui.cmbx_styles.setModel(AppStyleListModel(self))
        self.ui.cmbx_styles.currentIndexChanged.connect(self.on_cmbx_styles_current_index_changed)
        # 手动触发
        self.on_cmbx_styles_current_index_changed(0)
        self.ui.pbn_export.clicked.connect(self.on_pbn_export_clicked)
        self.ui.pbn_about.clicked.connect(self.on_pbn_about_clicked)

    def on_cmbx_styles_current_index_changed(self, index: int):
        model = self.ui.cmbx_styles.model()
        idx = model.index(index, 0)
        style = model.data(idx, QtCore.Qt.ItemDataRole.DisplayRole)
        QtWidgets.QApplication.setStyle(style)

    def sizeHint(self):
        return QtCore.QSize(800, 600)

    def on_pbn_export_clicked(self):
        reg_text = ["Windows Registry Editor Version 5.00"]
        pages = [self.ui.wg_chrome_page, self.ui.wg_edge_page, self.ui.wg_brave_page]
        for page in pages:
            reg_text.append(page.get_recommended_settings())
            reg_text.append(page.get_settings())
            reg_text.append(page.get_extensions())
            reg_text.append(page.get_search_engines())

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "保存", "..", "注册表文件(*.reg);;所有文件(*)")
        if len(filename) == 0:
            return

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n\n".join(reg_text))
        QtWidgets.QMessageBox.information(self, "信息", "已导出注册表文件。")

    def on_pbn_about_clicked(self):
        ver = f"{self.version[0]}.{self.version[1]}.{self.version[2]}"
        msg = f"一个用于生成以 Chromium 为内核的浏览器策略的注册表文件的工具。\n\n版本：{ver}，{self.version[-1]}"
        QtWidgets.QMessageBox.about(self, "关于", msg)
