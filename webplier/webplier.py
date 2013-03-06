#!/usr/bin/env python2.7
import os
import sys

from PyQt4.QtGui import *

from BrowserWindow import BrowserWindow
from QSingleApplication import QtSingleApplication
from SiteListWindow import SiteListWindow
import desktop
import errors


def main():
    if len(sys.argv) == 2:
        appid = sys.argv[1]
        app = QtSingleApplication(appid, [appid] + sys.argv[2:])
        if app.isRunning():
            sys.exit(0)
        errors.app = app
        desktopEntry = desktop.getEntry(appid)

        w = BrowserWindow(appid, desktopEntry.getBaseUrl(), desktopEntry.getName())
    else:
        appGuid = '3a34b884-8ab4-4a60-a243-dae69928a82e'
        app = QtSingleApplication(appGuid, ['Webplier'] + sys.argv[2:])
        if app.isRunning():
            sys.exit(0)
        w = SiteListWindow()
    w.show()
    app.setActivationWindow(w)

    sys.exit(app.exec_())

script = os.path.abspath(__file__)

if __name__ == '__main__':
    main()


