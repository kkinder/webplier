"""
Grabs icons from websites
"""
from urlparse import urlparse, urlunparse

from PyQt4.QtCore import QUrl, pyqtSignal, QByteArray, QObject, QString
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager
from PyQt4.QtWebKit import QWebPage, qWebKitVersion

FETCHER_USER_AGENT = 'Mozilla/5.0 (Linux) AppleWebKit/534.34 (KHTML, like Gecko) Webplier-fetcher/1.0.1' % (
    qWebKitVersion())

# This specifies how we look for icons. We go through this list, and for the first matching element, we use that icon.
# Format is:
# (element name, required properties, link property)
ELEMENT_SEARCHES = [
    ('link', {'rel': 'webapp-icon'}, 'href'),
    ('link', {'rel': 'fluid-icon'}, 'href'),

    # fucking apple...
    ('link', {'rel': 'apple-touch-icon', 'sizes': '144x144'}, 'href'),
    ('link', {'rel': 'apple-touch-icon', 'sizes': '114x114'}, 'href'),
    ('link', {'rel': 'apple-touch-icon-precomposed', 'sizes': '144x144'}, 'href'),
    ('link', {'rel': 'apple-touch-icon-precomposed', 'sizes': '114x114'}, 'href'),
    ('link', {'rel': 'apple-touch-icon', 'sizes': '72x72'}, 'href'),
    ('link', {'rel': 'apple-touch-icon', 'sizes': '57x57'}, 'href'),
    ('link', {'rel': 'apple-touch-icon-precomposed', 'sizes': '72x72'}, 'href'),
    ('link', {'rel': 'apple-touch-icon-precomposed', 'sizes': '57x57'}, 'href'),

    # If all else fails, favicon
    ('link', {'rel': 'shortcut icon'}, 'href'),
    ]

class IconGrabber(QObject):
    def __init__(self, url, callback, directLink=False):
        super(IconGrabber, self).__init__()
        parsedUrl = urlparse(url)

        self.url = url
        self.iconUrl = None
        self.callback = callback

        if directLink:
            self.tryList = []
            self.iconUrl = url
            self.page = QWebPage()
            self._downloadIcon()
        else:
            # What to try if we can't figure out the icon by parsing the page's HTML
            self.tryList = [
                urlunparse((parsedUrl.scheme, parsedUrl.netloc, '/favicon.png', '', '', '')),
                urlunparse((parsedUrl.scheme, parsedUrl.netloc, '/favicon.ico', '', '', '')),
                ]

            if parsedUrl.hostname.startswith('www'):
                self.tryList.append('http://icons.webplier.com/icons/%s.png' % parsedUrl.hostname.split('.', 1)[-1])
            else:
                self.tryList.append('http://icons.webplier.com/icons/%s.png' % parsedUrl.hostname)

            self.page = QWebPage()
            self.page.loadFinished.connect(self._loadFinished)
            self.page.mainFrame().load(QUrl(url))

    def _loadFinished(self):
        frame = self.page.mainFrame()

        iconFound = False

        for elementName, requiredProperties, linkProperty in ELEMENT_SEARCHES:
            if iconFound:
                break
            for e in frame.findAllElements(elementName):
                rejected = False
                for k, v in requiredProperties.items():
                    if unicode(e.attribute(k)).lower() != unicode(v).lower():
                        rejected = True
                        break
                if not rejected:
                    icon = e.attribute(linkProperty)
                    if icon:
                        self.iconUrl = icon
                        iconFound = True
                        break

        self.page.deleteLater()
        if not self.iconUrl:
            self._tryFromList()
        else:
            self._downloadIcon()
        frame.deleteLater()

    def _tryFromList(self):
        if self.tryList:
            self.iconUrl = self.tryList.pop(0)
            self._downloadIcon()
        else:
            self.callback(self.url, None, None)

    def _downloadIcon(self):
        url = QUrl(self.iconUrl)
        self.iconrequest = QNetworkRequest(url)
        self.iconrequest.setRawHeader("User-Agent", FETCHER_USER_AGENT)

        self.networkManager = QNetworkAccessManager()

        self.reply = self.networkManager.get(self.iconrequest)
        self.reply.finished.connect(self._downloadIconFinished)
        self.reply.error.connect(self._downloadIconError)

    def _downloadIconFinished(self):
        status = self.reply.attribute(QNetworkRequest.HttpStatusCodeAttribute).toInt()[0]

        if status in (301, 302):
            self.iconUrl = unicode(self.reply.header(QNetworkRequest.LocationHeader).toString())
            self._downloadIcon()
        elif status == 200:
            contentType = unicode(self.reply.header(QNetworkRequest.ContentTypeHeader).toString()).split(';')[0]
            if contentType.startswith('image') or contentType == 'application/octet-stream':
                self.callback(self.url, self.iconUrl, self.reply.readAll())
            else:
                self._downloadIconError()
        else:
            self._downloadIconError()

    def _downloadIconError(self):
        return self._tryFromList()

    def __del__(self):
        try:
            self.page.deleteLater()
        except RuntimeError:
            pass
        
        try:
            self.iconrequest.deleteLater()
        except RuntimeError:
            pass


if __name__ == '__main__':
    from PyQt4.QtGui import QApplication, QMessageBox
    import sys
    url = 'http://github.com'
    app = QApplication(sys.argv)
    x = IconGrabber(url)
    app.exec_()

