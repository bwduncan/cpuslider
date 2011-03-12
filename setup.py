#!/usr/bin/env python

from distutils.core import setup
from subprocess import Popen, PIPE
from PyQt4 import uic
import sys


def git_describe(abbrev=4):
    proc = Popen(['git', 'describe', '--abbrev=%d' % abbrev], stdout=PIPE)
    return proc.communicate()[0].strip()

if len(sys.argv) > 1 and sys.argv[1] == 'build':
    with open('cpusliderwindow.py', 'w') as f:
        uic.compileUi('cpuslider.ui', f)

setup(name="cpuslider",
      description="A simple slider application to control cpufreq in Linux",
      version=git_describe(),
      scripts=['cpuslider.py'],
      py_modules=['cpusliderwindow'],
      author="Bruce Duncan",
      author_email="bwduncan@gmail.com",
      url="http://github.com/bwduncan/cpuslider",
     )
