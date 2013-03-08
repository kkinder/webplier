import os
import sys

from PyQt4.QtCore import Qt, QString, QFile, QFileSystemWatcher
from PyQt4.QtGui import *

from i18n import tr, APP_NAME
from icongrabber import IconGrabber
from ui.SiteEditor import Ui_SiteEditor
import desktop
import errors

class SiteEditorWindow(QWidget, Ui_SiteEditor):
    def __init__(self, desktopEntry, isNew=False, isWidget=False, listItem=None):
        """

        :param desktopEntry: Desktop entry this editor should modify.
        :type desktopEntry: desktop.WebDesktopEntry or None
        """
        super(SiteEditorWindow, self).__init__()
        self.listItem = listItem
        self.setupUi(self)
        if desktopEntry:
            assert isinstance(desktopEntry, desktop.WebDesktopEntry)

        self.fetcher = None
        self.imageUnscaled = None
        self.needsSaving = False
        self._lastIconPath = ''

        self.desktopEntry = desktopEntry
        self.isNew = isNew
        self.isWidget = isWidget

        self.saveButton = self.newButtonBox.button(self.newButtonBox.Save)
        self.discardButton = self.newButtonBox.button(self.newButtonBox.Discard)

        self._refreshFromDesktopEntry()

        # Set up events
        self.saveButton.clicked.connect(self._save)
        self.discardButton.clicked.connect(self._discard)
        self.browseButton.clicked.connect(self._browse)
        self.closeButton = self.existingButtonBox.button(self.existingButtonBox.Close)

        self.urlLineEdit.editingFinished.connect(self._urlEditingFinished)
        self.iconLocationLineEdit.editingFinished.connect(self._iconLocationLineEditFinished)

        # Handle having this in its own window differently, and having it as a new app differently.
        if isWidget or not isNew:
            self.nameLineEdit.editingFinished.connect(self._interactiveSave)
            self.urlLineEdit.editingFinished.connect(self._interactiveSave)
            self.iconLocationLineEdit.editingFinished.connect(self._interactiveSave)

        if isWidget:
            self.existingButtonBox.hide()
            self.newButtonBox.hide()
        else:
            if isNew:
                self.existingButtonBox.hide()
                if not self.isWidget:
                    self.setWindowTitle(tr('SiteEditorWindow', 'Create web app'))
            else:
                self.newButtonBox.hide()
                if not self.isWidget:
                    self.setWindowTitle(tr('SiteEditorWindow', 'Edit web app: %s' % self.desktopEntry.get('Name')))
                self.closeButton.clicked.connect(self.hide)

        self.nameLineEdit.focusWidget()
        self.desktopEntry.onRefresh = self._refreshFromDesktopEntry
        self.nameLineEdit.setFocus()

    def _refreshFromDesktopEntry(self):
        self.urlLineEdit.setText(self.desktopEntry.getBaseUrl(''))
        self.nameLineEdit.setText(self.desktopEntry.get('Name', ''))
        iconPath = self.desktopEntry.get('Icon', '')
        if iconPath and os.path.exists(iconPath):
            self.iconLocationLineEdit.setText(iconPath)
            self.refreshIconPreview()
            self._lastIconPath = iconPath

    def _urlEditingFinished(self):
        url = unicode(self.urlLineEdit.text())

        if url != unicode(self.desktopEntry.getBaseUrl):
            if not (url.startswith('http://') or url.startswith('https://')):
                url = 'http://%s' % url
                self.urlLineEdit.setText(url)

            if url and '.' in url and not unicode(self.iconLocationLineEdit.text()).strip():
                self.iconStatusLabel.setText(tr('SiteEditorWindow', 'Finding icon...'))
                self.grabber = IconGrabber(url, self._onIconFound)

    def _iconLocationLineEditFinished(self):
        url = unicode(self.iconLocationLineEdit.text())

        if url != self._lastIconPath:
            self._fetchIcon()
            self._lastIconPath = url

    def _fetchIcon(self):
        url = unicode(self.iconLocationLineEdit.text())
        if url:
            self.iconStatusLabel.setText(tr('SiteEditorWindow', 'Finding icon...'))
            self.grabber = IconGrabber(url, self._onIconFound, directLink=True)

    def _onIconFound(self, siteUrl, iconUrl, icon):
        try:
            self.iconStatusLabel.setText(tr('SiteEditorWindow', ''))
        except RuntimeError:
            return
        if siteUrl == unicode(self.urlLineEdit.text()) or siteUrl == unicode(self.iconLocationLineEdit.text()):
            if iconUrl and icon and icon.length():
                self.iconStatusLabel.setText('')
                # If the URL has changed, nevermind.
                self.image = QPixmap()
                self.image.loadFromData(icon)
                self.image = self.image.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                self.imageUnscaled = QPixmap()
                self.imageUnscaled.loadFromData(icon)

                self.iconPreviewLabel.setPixmap(self.image)
                self.iconLocationLineEdit.setText(QString(iconUrl))
                self._lastIconPath = unicode(iconUrl)
                if self.listItem:
                    self.listItem.setIcon(QIcon(self.image))

                if self.isWidget:
                    self._interactiveSave()
            else:
                self.imageUnscaled = None
                self.iconLocationLineEdit.setText('')
                self.iconPreviewLabel.setPixmap(QPixmap())
                self.iconStatusLabel.setText(tr('SiteEditorWindow', 'No suitable icon found'))
                if self.listItem:
                    self.listItem.setIcon(QIcon.fromTheme('document-new'))
            if self.isWidget or not self.isNew:
                self._interactiveSave()

    def _interactiveSave(self):
        if unicode(self.nameLineEdit.text()).strip() and unicode(self.urlLineEdit.text()).strip():
            self._save(close=False)
        else:
            self.needsSaving = True

    def _save(self, close=True):
        if not self.desktopEntry.hasKey('Categories'):
            self.desktopEntry.set('Categories', 'Application;Network')

        if self.imageUnscaled:
            filename = os.path.join(desktop.dataPath(), '%s.png' % self.desktopEntry.appid)
            self.imageUnscaled.save(filename, 'PNG')
            self.desktopEntry.set('Icon', filename)
        elif self.iconLocationLineEdit.text() and os.path.exists(unicode(self.iconLocationLineEdit.text())):
            self.desktopEntry.set('Icon', unicode(self.iconLocationLineEdit.text()))
        else:
            self.desktopEntry.set('Icon', '')

        self.desktopEntry.setName(unicode(self.nameLineEdit.text()))
        self.desktopEntry.setBaseUrl(unicode(self.urlLineEdit.text()))
        self.desktopEntry.write()

        self.needsSaving = False

        if close:
            self.close()

    def _browse(self):
        file = QFileDialog.getOpenFileName(self,
                                           tr('SiteEditorWindow', 'Select icon'),
                                           os.getcwd(),
                                           tr('SiteEditorWindow', 'Images (*.png *.jpg)'))
        self.iconLocationLineEdit.setText(file)
        self.refreshIconPreview()
        if self.isWidget or not self.isNew:
            self._interactiveSave()

    def refreshIconPreview(self):
        self.image = QPixmap(self.iconLocationLineEdit.text())
        self.image = self.image.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.iconPreviewLabel.setPixmap(self.image)

        if self.listItem:
            self.listItem.setIcon(QIcon(self.image))

    def _discard(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    errors.app = app
    w = SiteEditorWindow(desktop.getEntry(desktop.generateAppid()), True)
    w.show()
    sys.exit(app.exec_())
