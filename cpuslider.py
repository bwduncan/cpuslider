#!/usr/bin/env python

from cpusliderwindow import Ui_cpuSliderWindow
import sys
from functools import partial
from PyQt4 import QtGui, QtCore

CPUFREQ = '/sys/devices/system/cpu/cpu0/cpufreq/'


class CPUSlider(QtGui.QMainWindow):
    def __init__(self):
        super(CPUSlider, self).__init__()

        self.ui = Ui_cpuSliderWindow()
        self.ui.setupUi(self)
        self.setup()
        self.refresh()

    def setup(self):
        self.statusLabel = QtGui.QLabel()
        self.ui.statusbar.addWidget(self.statusLabel)
        self.layout = QtGui.QGridLayout()
        with open(CPUFREQ + 'scaling_available_governors') as f:
            governors = f.read().split()
        self.buttons = []
        for i, line in enumerate(governors):
            button = QtGui.QRadioButton(line)
            self.layout.addWidget(button, i, 0)
            self.layout.setRowStretch(i, 1)
            self.connect(button, QtCore.SIGNAL('toggled(bool)'),
                         partial(self.buttonToggled, line))
            self.buttons.append(button)
        with open(CPUFREQ + 'scaling_available_frequencies') as f:
            self.freqs = f.read().split()
        with open(CPUFREQ + 'scaling_cur_freq') as f:
            cur_freq = f.read().strip()
        self.slider = QtGui.QSlider(QtCore.Qt.Vertical)
        self.slider.setMaximum(len(self.freqs) - 1)  # minimum defaults to 0
        # The value will be set in refresh.
        self.layout.addWidget(self.slider, 0, 1, len(governors) - 1, 1)
        self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'),
                     self.updateLabel)

        self.label = QtGui.QLabel("%.1fGHz" % (float(cur_freq) / 1e6))
        self.layout.addWidget(self.label, len(governors) - 1, 1)
        self.ui.groupBox.setLayout(self.layout)

    def refresh(self):
        # Set the status bar to the current governor
        with open(CPUFREQ + 'scaling_governor') as f:
            governor = f.read().strip()
        self.statusLabel.setText(governor)
        with open(CPUFREQ + 'scaling_available_governors') as f:
            governors = f.read().split()
        # Remove governors which no longer exist
        for button in self.buttons:  # TODO Can't test this easily...
            if button.text() not in governors:
                button.deleteLater()
                self.buttons.remove(button)
            elif button.text() == governor:
                button.setChecked(True)
        with open(CPUFREQ + 'scaling_available_frequencies') as f:
            self.freqs = f.read().split()
        # Set the slider bar to the current frequency.
        with open(CPUFREQ + 'scaling_cur_freq') as f:
            freq = f.read().strip()
        # Set the slider value without invoking updateLabel, because it
        # changes the governor and the frequency.
        self.disconnect(self.slider, QtCore.SIGNAL('valueChanged(int)'),
                    self.updateLabel)
        self.slider.setValue(len(self.freqs) - self.freqs.index(freq) - 1)
        self.connect(self.slider, QtCore.SIGNAL('valueChanged(int)'),
                     self.updateLabel)
        if governor in ("userspace", "powersave", "performance"):
            self.label.setText("%.1fGHz" % (float(freq) / 1e6))
        else:
            self.label.setText("Dynamic")

    def updateLabel(self, value):
        new_freq = self.freqs[-value - 1]
        with open(CPUFREQ + 'scaling_governor') as f:
            governor = f.read().strip()
        if governor in ("userspace", "powersave", "performance"):
            self.label.setText("%.1fGHz" % (float(new_freq) / 1e6))
        else:
            self.label.setText("Dynamic")
        if governor != "userspace":
            with open(CPUFREQ + 'scaling_governor', 'w') as f:
                f.write("userspace\n")
            for button in self.buttons:
                if button.text() == "userspace":
                    button.setChecked(True)
        with open(CPUFREQ + 'scaling_setspeed', 'w') as f:
            f.write(new_freq + '\n')

    def buttonToggled(self, name, checked):
        if checked:
            with open(CPUFREQ + 'scaling_governor', 'w') as f:
                f.write(name + '\n')
            self.refresh()


def main():
    app = QtGui.QApplication(sys.argv)

    mainwindow = CPUSlider()
    mainwindow.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
