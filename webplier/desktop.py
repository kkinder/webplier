"""
Utility functions for dealing with FreeDesktop.org desktop entries.
"""
from functools import partial
import os
import uuid
import xdg.BaseDirectory
import xdg.DesktopEntry
from PyQt4.QtCore import QFileSystemWatcher
import time

import errors

from i18n import tr, APP_NAME

FREEDESKTOP_ORG_RESOURCE_NAME = APP_NAME.lower()

def dataPath():
    path = None
    for path in xdg.BaseDirectory.load_data_paths(FREEDESKTOP_ORG_RESOURCE_NAME):
        break
    if not (path and os.path.exists(path)):
        path = xdg.BaseDirectory.save_data_path(FREEDESKTOP_ORG_RESOURCE_NAME)
    assert os.path.exists(path) and os.path.isdir(path)
    return path

class WebDesktopEntry(xdg.DesktopEntry.DesktopEntry):
    def __init__(self, appid, *args, **kwargs):
        import webplier

        self.appid = appid
        xdg.DesktopEntry.DesktopEntry.__init__(self, *args, **kwargs)

        self.setWindowWidth = partial(xdg.DesktopEntry.DesktopEntry.set, self, 'X-%s-Window-Width' % APP_NAME)
        self.getWindowWidth = partial(xdg.DesktopEntry.DesktopEntry.get, self, 'X-%s-Window-Width' % APP_NAME)
        self.setWindowHeight = partial(xdg.DesktopEntry.DesktopEntry.set, self, 'X-%s-Window-Height' % APP_NAME)
        self.getWindowHeight = partial(xdg.DesktopEntry.DesktopEntry.get, self, 'X-%s-Window-Height' % APP_NAME)

        self.setBaseUrl = partial(xdg.DesktopEntry.DesktopEntry.set, self, 'X-%s-BaseUrl' % APP_NAME)
        self.getBaseUrl = partial(xdg.DesktopEntry.DesktopEntry.get, self, 'X-%s-BaseUrl' % APP_NAME)

        self.setName = partial(xdg.DesktopEntry.DesktopEntry.set, self, 'Name')

        if not self.hasGroup('Desktop Entry'):
            self.addGroup('Desktop Entry')

        if not self.get('Exec'):
            self.set('Exec', 'plier %s' % (self.appid,))

        self.set('X-%s-Type' % APP_NAME, 'Webapp')
        self.set('X-%s-AppId' % APP_NAME, appid)

        # TODO: Get this working.

        self.watcher = QFileSystemWatcher()
        self.addPath(getPath('%s-%s.desktop' % (APP_NAME.lower(), self.appid)))
        self.watcher.fileChanged.connect(self._refreshFromFilesystem)

        self.onRefresh = None

    def _refreshFromFilesystem(self):
        path = getPath('%s-%s.desktop' % (APP_NAME.lower(), self.appid))
        if not (os.path.exists(path) and len(open(path).read()) > 1):
            return

        self.parse(path)
        if self.onRefresh:
            self.onRefresh()

        self.watcher.removePath(path)
        self.addPath(path)

    def write(self, *args, **kwargs):
        path = getPath('%s-%s.desktop' % (APP_NAME.lower(), self.appid))
        self.watcher.removePath(path)
        v = xdg.DesktopEntry.DesktopEntry.write(self, *args, **kwargs)
        self.addPath(path)
        return v

    @classmethod
    def fromPath(cls, path):
        de = xdg.DesktopEntry.DesktopEntry(path)
        appid = de.get('X-%s-AppId' % APP_NAME)
        return cls(appid, path)

    def addPath(self, path):
        self.watcher.addPath(path)

    @classmethod
    def getAll(cls):
        """
        Returns all found desktop entries that are webapps we created.
        """
        # TODO: Should we hardcode ".desktop"?
        path = getPath()
        filenames = filter(lambda x: x.endswith('.desktop'), os.listdir(path))
        filenames = map(lambda x: os.path.join(path, x), filenames)
        filenames = filter(cls.isWebDesktopEntry, filenames)

        return map(cls.fromPath, filenames)

    @classmethod
    def isWebDesktopEntry(cls, filename):
        de = xdg.DesktopEntry.DesktopEntry(filename)
        if de.hasKey('X-%s-Type' % APP_NAME) and de.get('X-%s-Type' % APP_NAME) == 'Webapp':
            return True
        else:
            return False


def getPath(filename=None):
    """
    Returns the full path of a new or existing desktop file.

    If filename is None, return the path to where the file would be.
    """
    directory = None

    for d in xdg.BaseDirectory.xdg_data_dirs:
        d = os.path.join(d, 'applications')
        if os.access(d, os.W_OK):
            directory = d
            break

    if not directory:
        for d in xdg.BaseDirectory.xdg_data_dirs:
            if os.access(d, os.W_OK):
                directory = os.path.join(d, 'applications')
                os.mkdir(directory)
                break

    if not directory:
        errors.showError(tr('None', 'Unable to find desktop menu folder'),
                         tr('None', '%s was unable to find where you store your FreeDesktop.org menu items. Perhaps ' \
                            'you are not running a FreeDesktop.org-compliant desktop?' % APP_NAME))
        return

    if filename:
        return os.path.realpath(os.path.join(directory, filename))
    else:
        return directory

def getEntry(appid):
    path = getPath('%s-%s.desktop' % (APP_NAME.lower(), appid))
    return WebDesktopEntry(appid, path)

def generateAppid():
    return uuid.uuid4().get_hex()

