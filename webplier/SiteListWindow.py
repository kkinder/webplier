import os

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QIcon, QSizePolicy, QGridLayout, QListWidgetItem, QMessageBox, QDialog

from PersistableCookieJar import PersistableCookieJar
from QSingleApplication import QtSingleApplication
import about
import desktop
from i18n import DATE, VERSION, APP_NAME, ABOUT_TEXT, tr
from ui.SiteList import Ui_SiteList
from SiteEditorWindow import SiteEditorWindow
import resources

class SiteListWindow(QDialog, Ui_SiteList):
    def __init__(self):
        """

        :param desktopEntry: Desktop entry this editor should modify.
        :type desktopEntry: desktop.WebDesktopEntry
        """
        super(SiteListWindow, self).__init__()
        self.setupUi(self)

        # self.siteEditor = SiteEditorWindow(None, isWidget=True)
        # self.siteEditor.setupUi(self.siteEditorWidget)
        self.desktopEntry = None
        self.allEntries = []

        self.addButton.clicked.connect(self._onAddSite)
        self.addButton.setIcon(QIcon.fromTheme('list-add'))
        self.removeButton.setIcon(QIcon.fromTheme('list-remove'))
        self.removeButton.clicked.connect(self._onRemoveSite)
        self.closeButton.clicked.connect(self.close)
        self.closeButton.setIcon(QIcon.fromTheme('window-close'))
        self.aboutButton.clicked.connect(lambda x: about.show(self))
        self.aboutButton.setIcon(QIcon.fromTheme('help-about'))

        self.setWindowIcon(QIcon(':appicon'))

        self.rescan()

        self.siteListWidget.currentItemChanged.connect(self._itemActivated)

    def _itemActivated(self, item, old):
        if item:
            appid = item.data(Qt.UserRole).toPyObject()
            de = None
            for i in self.allEntries:
                if i.appid == appid:
                    de = i

            if not de:
                de = desktop.getEntry(appid)

            self.desktopEntry = de

            self._refreshEditor()
        else:
            self.desktopEntry = None
            self._refreshEditor()

    def rescan(self):
        """
        Scans desktop entries for one of ours.
        """
        self.allEntries = desktop.WebDesktopEntry.getAll()
        for e in self.allEntries:
            if os.path.exists(e.get('Icon')):
                icon = QIcon(e.get('Icon'))
            else:
                icon = QIcon.fromTheme('document-new')
            i = QListWidgetItem(icon, e.get('Name'), self.siteListWidget)
            i.setData(Qt.UserRole, e.appid)

    def _onAddSite(self):
        if self.desktopEntry:
            pass
            #self.desktopEntry.write()

        self.desktopEntry = desktop.getEntry(desktop.generateAppid())
        self.allEntries.append(self.desktopEntry)

        i = QListWidgetItem(tr('SiteEditorWindow', '<Untitled>'), self.siteListWidget)
        i.setData(Qt.UserRole, self.desktopEntry.appid)
        self.siteListWidget.setCurrentItem(i)

        # TODO: This seems like a very strange way of deleting one widget and replacing it with another.
        # Is there a better way?
        self._refreshEditor()

    def _onRemoveSite(self):
        i = self.siteListWidget.currentItem()
        if i:
            appid = unicode(i.data(Qt.UserRole).toPyObject())
            if QtSingleApplication.isOtherRunning(appid):
                QMessageBox.information(self,
                                        tr('SiteEditorWindow', 'Cannot delete app'),
                                        tr('SiteEditorWindow', 'You cannot delete an app while it is running'))
                return

            name = unicode(i.text())
            answer = QMessageBox.warning(
                self,
                tr('SiteEditorWindow', 'Are you sure you want to delete web app?'),
                tr('SiteEditorWindow', '<strong>Are you sure you want to delete %s?</strong><br/><br/>'
                                       'All cookies, preferences, and other stored data associated will be deleted.' % name),
                QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.siteListWidget.removeItemWidget(i)
                desktopPath = desktop.getPath('%s-%s.desktop' % (APP_NAME.lower(), appid))
                if os.path.exists(desktopPath):
                    os.remove(desktopPath)
                iconPath = os.path.join(desktop.dataPath(), '%s.png' % self.desktopEntry.appid)
                if os.path.exists(iconPath):
                    os.remove(iconPath)
                jar = PersistableCookieJar(identifier=appid)
                jar.deleteFilesThreaded()
                self.siteListWidget.takeItem(self.siteListWidget.row(i))

    def _refreshEditor(self):
        self.verticalLayout_3.removeWidget(self.siteEditorWidget)
        self.siteEditorWidget.deleteLater()

        self.siteEditorWidget = QWidget(self)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.siteEditorWidget.sizePolicy().hasHeightForWidth())
        self.siteEditorWidget.setSizePolicy(sizePolicy)
        self.siteEditorLayout = QGridLayout()
        self.siteEditorWidget.setLayout(self.siteEditorLayout)
        self.verticalLayout_3.insertWidget(0, self.siteEditorWidget)

        if self.desktopEntry:
            self.siteEditor = SiteEditorWindow(self.desktopEntry, isWidget=True,
                                               listItem=self.siteListWidget.currentItem())
            self.siteEditorLayout.addWidget(self.siteEditor, 0, 0)
            self.siteEditor.nameLineEdit.textChanged.connect(self._onNameChange)

    def _onNameChange(self):
        self.siteListWidget.currentItem().setText(self.siteEditor.nameLineEdit.text() or
                                                  tr('SiteEditorWindow', '<Untitled>'))