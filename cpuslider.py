#!/usr/bin/env python

from cpusliderwindow import Ui_cpuSliderWindow
import sys
from PyQt4 import QtGui, QtCore

CPUFREQ = '/sys/devices/system/cpu/cpu0/cpufreq/'


class CPUSlider(QtGui.QMainWindow):
    def __init__(self):
        super(CPUSlider, self).__init__()

        self.ui = Ui_cpuSliderWindow()
        self.ui.setupUi(self)
        self.refresh()

    def refresh(self):
        with open(CPUFREQ + 'scaling_governor') as f:
            governor = f.read().strip()
        self.ui.statusbar.addWidget(QtGui.QLabel(governor))
        with open(CPUFREQ + 'scaling_available_governors') as f:
            layout = QtGui.QGridLayout()
            governors = f.read().split()
            for i, line in enumerate(governors):
                button = QtGui.QRadioButton(line)
                if governor == line:
                    button.setChecked(True)
                layout.addWidget(button, i, 0)
                layout.setRowStretch(i, 1)
            if governor == "userspace":
                with open(CPUFREQ + 'scaling_available_frequencies') as f:
                    self.freqs = f.read().split()
                with open(CPUFREQ + 'scaling_cur_freq') as f:
                    cur_freq = f.read().strip()
                slider = QtGui.QSlider(QtCore.Qt.Vertical)
                slider.setMaximum(len(self.freqs) - 1)  # minimum defaults to 0
                layout.addWidget(slider, 0, 1, len(governors) - 1, 1)
                self.connect(slider, QtCore.SIGNAL('valueChanged(int)'),
                             self.updateLabel)

                self.label = QtGui.QLabel("%.1fGHz" % (float(cur_freq) / 1e6))
                layout.addWidget(self.label, len(governors) - 1, 1)
            self.ui.groupBox.setLayout(layout)

    def updateLabel(self, value):
        new_freq = self.freqs[-value - 1]
        with open(CPUFREQ + 'scaling_setspeed', 'w') as f:
            f.write(new_freq + '\n')
        self.label.setText("%.1fGHz" % (float(new_freq) / 1e6))


def main():
    app = QtGui.QApplication(sys.argv)

    mainwindow = CPUSlider()
    mainwindow.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
