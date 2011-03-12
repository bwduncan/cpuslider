#!/usr/bin/env python

from cpusliderwindow import Ui_cpuSliderWindow
import sys
from PyQt4 import QtGui

class CPUSlider(QtGui.QMainWindow):
    def __init__(self):
        super(CPUSlider, self).__init__()

        self.ui = Ui_cpuSliderWindow()
        self.ui.setupUi(self)


def main():
    app = QtGui.QApplication(sys.argv)

    mainwindow = CPUSlider()
    mainwindow.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
