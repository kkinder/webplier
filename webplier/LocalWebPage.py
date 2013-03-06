import webbrowser
from PyQt4.QtWebKit import QWebPage


class LocalWebPage(QWebPage):
    def triggerAction(self, action, checked=False):
        if action == QWebPage.OpenLinkInNewWindow:
            url = unicode(self.mainFrame().url().toString())
            webbrowser.open(url, 1)
        else:
            return super(LocalWebPage, self).triggerAction(action, checked)