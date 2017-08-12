#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Notes:
# 1.install from egg file
# gen egg: python setup.py bdist_egg
# install: pip install dist/*.egg
# 2.install from exec setup.py
# 1) install:
#    sudo python setup.py install --record install.txt
# 2) remove:
#    cat install.txt | xargs sudo rm -rf
#
import os
from setuptools import setup
from setuptools.command.install import install

LOGIN_USER = os.getlogin()
CURRENT_DIR = os.getcwd()
execfile('%s/src/lib/common.py' % CURRENT_DIR)


class CustomInstallCommand(install):
    def run(self):
        print "Sart install :)"
        install.run(self)
        self.service_handle()
        self.indicator_handle()
        print "Finish install :)"

    def service_handle(self):
        source = '%s/%s' % (SYSTEMD_DIR, SERVICE_FILENAME)
        target = '%s/%s' % (SYSTEMD_USER_DIR, SERVICE_FILENAME)
        cmd1 = 'sed -i "s/xxx/%s/" %s' % (LOGIN_USER, source)
        cmd2 = 'ln -sf %s %s' % (source, target)
        cmd = '%s && %s' % (cmd1, cmd2)
        shell_exec(cmd)

    def indicator_handle(self):
        cmd = 'chown %s:%s %s/%s' % (LOGIN_USER, LOGIN_USER, AUTOSTART_DIR, DESKTOP_FILENAME)
        shell_exec(cmd)


setup(
    name="DictHub",
    version="0.1.0",
    zip_safe=False,

    description="A Simple App Indicator For Ubuntu",
    long_description="A simple app for storing dict and sentence.",
    author="hanson",
    author_email="liangguohuan@gmail.com",

    license="MIT",
    keywords=("dict", "dicthub"),
    platforms="Ubuntu",
    url="https://github.com/liangguohuan/DictHub",
    packages=['DictHub', ],
    package_dir={"DictHub": "src/lib"},
    package_data={"DictHub": ["data/*"]},
    data_files=[(ICON_THEM_PATH, ["config/dict-indicator.svg"]),
                (SYSTEMD_DIR, ["config/systemd/%s" % SERVICE_FILENAME]),
                (AUTOSTART_DIR, ["config/%s" % DESKTOP_FILENAME])],
    install_requires=[
        'click>=6.6',
    ],
    entry_points={
        'console_scripts': [
            'dicthub = DictHub.command:main',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
)
