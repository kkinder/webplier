import thread
import shutil
import os

from PyQt4.QtCore import QByteArray
from PyQt4.QtNetwork import QNetworkCookieJar, QNetworkCookie

import desktop


class PersistableCookieJar(QNetworkCookieJar):
    def __init__(self, parent=None, identifier='shared'):
        super(PersistableCookieJar, self).__init__(parent)
        self.identifier = identifier
        self._isDeleted = False

    def _getLocalDataPath(self):
        # Figure out our freedesktop.org data path (probably ~/.local/share/whatnot)
        dataDir = desktop.dataPath()

        webDataPath = os.path.join(dataDir, 'web-data')
        if not os.path.exists(webDataPath):
            os.mkdir(webDataPath)

        localDataPath = os.path.join(webDataPath, self.identifier)
        if not os.path.exists(localDataPath):
            os.mkdir(localDataPath)
        return localDataPath

    def _cookiesFilePath(self):
        localDataPath = self._getLocalDataPath()

        cookieFile = os.path.join(localDataPath, 'cookies.txt')
        return cookieFile

    def load(self):
        cookieFile = self._cookiesFilePath()

        if os.path.exists(cookieFile):
            if os.stat(cookieFile).st_size:
                self.setAllCookies(QNetworkCookie.parseCookies(QByteArray(open(cookieFile).read())))
        else:
            self.setAllCookies([])

    def save(self):
        if self._isDeleted:
            return

        cookieFile = self._cookiesFilePath()

        items = []
        for c in self.allCookies():
            items.append(unicode(c.toRawForm()))

        open(cookieFile, 'wb').write('\n'.join(items))

    def setCookiesFromUrl(self, list_of_QNetworkCookie, QUrl):
        returnValue = super(PersistableCookieJar, self).setCookiesFromUrl(list_of_QNetworkCookie, QUrl)
        self.save()
        return returnValue

    def deleteFiles(self):
        path = self._getLocalDataPath()
        shutil.rmtree(path, ignore_errors=True)

    def deleteFilesThreaded(self):
        thread.start_new_thread(self.deleteFiles, tuple())
