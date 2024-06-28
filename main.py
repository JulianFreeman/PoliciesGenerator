# coding: utf8
import sys
from PySide6 import QtWidgets
from mw_policies_gen import MwPoliciesGen

import rc_policies_gen

version = (0, 1, 0, 20240627)


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MwPoliciesGen(version)
    win.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
