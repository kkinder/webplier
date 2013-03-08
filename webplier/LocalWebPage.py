import webbrowser
from PyQt4.QtCore import QString
from PyQt4.QtWebKit import QWebPage, qWebKitVersion

BROWSER_USER_AGENT = 'Mozilla/5.0 (Linux) AppleWebKit/534.34 (KHTML, like Gecko) Webplier-browser/1.0' % (
    qWebKitVersion())

class LocalWebPage(QWebPage):
    def triggerAction(self, action, checked=False):
        if action == QWebPage.OpenLinkInNewWindow:
            url = unicode(self.mainFrame().url().toString())
            webbrowser.open(url, 1)
        else:
            return super(LocalWebPage, self).triggerAction(action, checked)

    def userAgentForUrl(self, url):
        return QString(BROWSER_USER_AGENT)
