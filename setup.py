#!/usr/bin/env python

from distutils.core import setup
from subprocess import Popen, PIPE


def git_describe(abbrev=4):
    proc = Popen(['git', 'describe'], stdout=PIPE)
    return proc.communicate()[0].strip()

setup(name="cpuslider",
      description="A simple slider application to control cpufreq in Linux",
      version=git_describe(),
      scripts=['cpuslider.py'],
      author="Bruce Duncan",
      author_email="bwduncan@gmail.com",
      url="http://github.com/bwduncan/cpuslider",
     )
