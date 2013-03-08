import webbrowser

from PyQt4.QtCore import QUrl, Qt, QMetaObject
from PyQt4.QtGui import QMainWindow, QApplication, QWidget, QGridLayout, QLineEdit, QProgressBar, QMenuBar, QMenu, QStatusBar, QToolBar, QAction, QIcon, QKeySequence, QShortcut, QPrinter, QPrintDialog, QDialog
from PyQt4.QtWebKit import QWebPage, QWebSettings

from LocalWebPage import LocalWebPage
from LocalWebView import LocalWebView
from PersistableCookieJar import PersistableCookieJar
from SiteEditorWindow import SiteEditorWindow
from i18n import tr, APP_NAME
import about
import desktop

# noinspection PyCallByClass,PyTypeChecker,PyOldStyleClasses
class BrowserWindow(QMainWindow):
    def retranslateUi(self):
        self.setWindowTitle(
            QApplication.translate("self", "self", None, QApplication.UnicodeUTF8))
        self.menuFile.setTitle(
            QApplication.translate("self", "&File", None, QApplication.UnicodeUTF8))
        self.menuView.setTitle(
            QApplication.translate("self", "&View", None, QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(
            QApplication.translate("self", "&Edit", None, QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(
            QApplication.translate("self", "&Help", None, QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(
            QApplication.translate("self", "toolBar", None, QApplication.UnicodeUTF8))
        self.actionHome.setText(
            QApplication.translate("self", "&Home", None, QApplication.UnicodeUTF8))
        self.actionHome.setToolTip(
            QApplication.translate("self", "Go Home", None, QApplication.UnicodeUTF8))
        self.actionShowMenu.setText(
            QApplication.translate("self", "Show &Menu", None, QApplication.UnicodeUTF8))
        self.actionShowToolbar.setText(
            QApplication.translate("self", "Show &Toolbar", None, QApplication.UnicodeUTF8))
        self.actionClose.setText(
            QApplication.translate("self", "&Close", None, QApplication.UnicodeUTF8))
        self.actionModifyWebapp.setText(
            QApplication.translate("self", "Modify &Webapp", None, QApplication.UnicodeUTF8))
        self.actionEditPreferences.setText(
            QApplication.translate("self", "Edit &Preferences", None, QApplication.UnicodeUTF8))
        self.actionPrint.setText(
            QApplication.translate("self", "&Print", None, QApplication.UnicodeUTF8))
        self.actionAbout.setText(
            QApplication.translate("self", "&About", None, QApplication.UnicodeUTF8))

    def __init__(self, appid, base, name):
        super(BrowserWindow, self).__init__()

        self.appid = appid
        self.name = name
        self.base = base

        # Main widgets
        self.centralwidget = QWidget(self)
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.urlLineEdit = QLineEdit(self)
        self.progressBar = QProgressBar(self)

        # Custom webview
        self.page = LocalWebPage()
        self.page.setFeaturePermission(self.page.mainFrame(), LocalWebPage.Notifications,
                                       LocalWebPage.PermissionGrantedByUser)
        self.webViewMain = LocalWebView(self.centralwidget)
        self.webViewMain.setPage(self.page)
        self.gridLayout_2.addWidget(self.webViewMain, 0, 0, 1, 1)

        self.menubar = QMenuBar(self)
        self.menuFile = QMenu(self.menubar)
        self.menuView = QMenu(self.menubar)
        self.menuEdit = QMenu(self.menubar)
        self.menuHelp = QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(self)
        self.toolBar.setMovable(False)
        self.toolBar.setFloatable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        # Create actions
        self.actionOpenLinkInNewWindow = self.page.action(self.page.OpenLinkInNewWindow)
        self.actionOpenLinkInNewWindow.setText(tr('BrowserWindow', 'Open in &Browser'))
        self.actionBack = self.page.action(self.page.Back)
        self.actionForward = self.page.action(self.page.Forward)
        self.actionStop = self.page.action(self.page.Stop)
        self.actionReload = self.page.action(self.page.Reload)
        self.actionHome = QAction(self)
        self.actionShowMenu = QAction(self)
        self.actionShowMenu.setCheckable(True)
        self.actionShowToolbar = QAction(self)
        self.actionShowToolbar.setCheckable(True)
        self.actionClose = QAction(self)
        self.actionModifyWebapp = QAction(self)
        self.actionEditPreferences = QAction(self)
        self.actionPrint = QAction(self)
        self.actionSaveLink = self.page.action(self.page.DownloadLinkToDisk)
        self.actionSaveLink.setEnabled(False)
        self.actionAbout = QAction(self)

        # Populate menu and toolbars
        self.menuFile.addAction(self.actionHome)
        self.menuFile.addAction(self.actionBack)
        self.menuFile.addAction(self.actionForward)
        self.menuFile.addAction(self.actionStop)
        self.menuFile.addAction(self.actionReload)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuView.addAction(self.actionShowMenu)
        self.menuView.addAction(self.actionShowToolbar)
        self.menuView.addSeparator()
        self.menuEdit.addAction(self.actionModifyWebapp)
        #self.menuEdit.addAction(self.actionEditPreferences)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionBack)
        self.toolBar.addAction(self.actionForward)
        self.toolBar.addWidget(self.urlLineEdit)

        self.toolBar.addAction(self.actionStop)
        self.toolBar.addAction(self.actionReload)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        self.setWindowTitle(self.name)

        # Set up cookie jar that persists sessions
        self.cookieJar = PersistableCookieJar(self, identifier=self.appid)
        self.cookieJar.load()
        self.webViewMain.page().networkAccessManager().setCookieJar(self.cookieJar)

        # Set up link delegation so that external links open in web browser.
        self.webViewMain.page().setLinkDelegationPolicy(QWebPage.DelegateExternalLinks)

        self.desktopEntry = desktop.getEntry(self.appid)

        # Set icons for actions; this can't be done in the designer, AFAICT
        self.actionHome.setIcon(QIcon.fromTheme('go-home'))
        self.actionAbout.setIcon(QIcon.fromTheme('help-about'))

        # Set up shortcuts
        self.actionStop.setShortcut(Qt.Key_Escape)
        self.actionBack.setShortcut(QKeySequence.Back)
        self.actionForward.setShortcut(QKeySequence.Forward)
        self.actionReload.setShortcut(QKeySequence.Refresh)
        self.actionHome.setShortcut('Ctrl+Home')
        self.actionShowMenu.setShortcut('Ctrl+m')
        self.actionShowToolbar.setShortcut('Ctrl+t')
        self.actionPrint.setShortcut(QKeySequence.Print)

        self.backShortcut = QShortcut(self)
        self.backShortcut.setKey(Qt.Key_Back)
        self.backShortcut.activated.connect(self.webViewMain.back)

        self.forwardShortcut = QShortcut(self)
        self.forwardShortcut.setKey(Qt.Key_Forward)
        self.forwardShortcut.activated.connect(self.webViewMain.forward)

        # Set up context menu
        self.webViewMain.setContextMenuPolicy(Qt.CustomContextMenu)
        self.webViewMain.customContextMenuRequested.connect(self.showMenu)

        # Setup statusbar and toolbar
        for c in self.statusBar().children()[0].children():
            c.removeWidget(c)
        self.statusBar().addPermanentWidget(self.progressBar, 1)

        self.actionShowToolbar.setChecked(True)
        self.actionShowMenu.setChecked(True)

        # Icon
        if self.desktopEntry.hasKey('Icon'):
            self.icon = QIcon(self.desktopEntry.get('Icon'))
            self.setWindowIcon(self.icon)
        else:
            self.webViewMain.iconChanged.connect(self.setWindowIcon)

        # Set up events
        if self.desktopEntry.get('X-%s-menu-enabled' % APP_NAME) == '0':
            self.actionShowMenu.setChecked(False)
        else:
            self.actionShowMenu.setChecked(True)
        if self.desktopEntry.get('X-%s-toolbar-enabled' % APP_NAME) == '0':
            self.actionShowToolbar.setChecked(False)
        else:
            self.actionShowToolbar.setChecked(True)

        self.webViewMain.linkClicked.connect(self._onLinkClick)
        self.webViewMain.titleChanged.connect(self.setWindowTitle)
        self.webViewMain.loadProgress.connect(self._setLoadingStatus)
        self.webViewMain.urlChanged.connect(lambda x: self.urlLineEdit.setText(x.toString()))
        self.page.printRequested.connect(self._onPrint)
        self.actionHome.triggered.connect(lambda x: self.webViewMain.load(QUrl(self.base)))
        self.actionClose.triggered.connect(self.close)
        self.actionPrint.triggered.connect(self._onPrint)
        self.urlLineEdit.returnPressed.connect(self._onUrlEdit)
        self.actionShowToolbar.triggered.connect(self._onShowToolbar)
        self.actionShowMenu.triggered.connect(self._onShowMenu)
        self.actionAbout.triggered.connect(lambda x: about.show(self))
        self.actionModifyWebapp.triggered.connect(self._onModify)

        self._onShowMenu()
        self._onShowToolbar()

        try:
            self.resize(int(self.desktopEntry.getWindowWidth()), int(self.desktopEntry.getWindowHeight()))
        except (ValueError, TypeError):
            self.resize(800, 600)

        # Load first page
        self.webViewMain.load(QUrl(base))

        self.editor = SiteEditorWindow(self.desktopEntry, isNew=False)

    def _onModify(self):
        self.editor.show()

    def closeEvent(self, qCloseEvent):
        self.desktopEntry.setWindowWidth(self.width())
        self.desktopEntry.setWindowHeight(self.height())
        self.desktopEntry.write()

    def _onPrint(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() != QDialog.Accepted:
            return
        self.page.mainFrame().print_(printer)

    def _setLoadingStatus(self, value):
        if value < 100:
            self.progressBar.setValue(value)
            self.progressBar.show()
            self.statusBar().show()
            self.actionReload.setVisible(False)
            self.actionStop.setVisible(True)
        else:
            self.page.setFeaturePermission(self.page.mainFrame(), LocalWebPage.Notifications,
                                           LocalWebPage.PermissionGrantedByUser)
            self.progressBar.hide()
            self.statusBar().hide()
            self.actionReload.setVisible(True)
            self.actionStop.setVisible(False)

    def _onUrlEdit(self):
        url = unicode(self.urlLineEdit.text())
        qurl = QUrl(url)
        if not qurl.scheme():
            qurl.setScheme('http')

        self.webViewMain.load(qurl)

    def _onLinkClick(self, qurl):
        url = unicode(qurl.toString())
        if not unicode(url).startswith(self.base):
            webbrowser.open(url, 1)
        else:
            self.webViewMain.load(qurl)

    def _onShowToolbar(self):
        if self.actionShowToolbar.isChecked():
            self.toolBar.show()
            self.desktopEntry.set('X-%s-toolbar-enabled' % APP_NAME, '1')
        else:
            self.toolBar.hide()
            self.desktopEntry.set('X-%s-toolbar-enabled' % APP_NAME, '0')

    def _onShowMenu(self):
        if self.actionShowMenu.isChecked():
            self.menubar.show()
            self.desktopEntry.set('X-%s-menu-enabled' % APP_NAME, '1')
        else:
            self.menubar.hide()
            self.desktopEntry.set('X-%s-menu-enabled' % APP_NAME, '0')

    def showMenu(self, point):
        m = self.webViewMain.page().createStandardContextMenu()

        # TODO: Make this less awful and fragile
        for a in m.actions():
            if a == self.actionSaveLink:
                m.removeAction(a)

        m.addSeparator()
        m.addAction(self.actionShowMenu)
        m.addAction(self.actionShowToolbar)
        globalpos = self.mapToParent(point)

        m.exec_(globalpos)