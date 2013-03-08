# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SiteEditor.ui'
#
# Created: Thu Mar  7 20:31:05 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SiteEditor(object):
    def setupUi(self, SiteEditor):
        SiteEditor.setObjectName(_fromUtf8("SiteEditor"))
        SiteEditor.resize(653, 472)
        self.gridLayout = QtGui.QGridLayout(SiteEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.browseButton = QtGui.QPushButton(SiteEditor)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.gridLayout_2.addWidget(self.browseButton, 6, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem1, 4, 2, 1, 1)
        self.nameLineEdit = QtGui.QLineEdit(SiteEditor)
        self.nameLineEdit.setObjectName(_fromUtf8("nameLineEdit"))
        self.gridLayout_2.addWidget(self.nameLineEdit, 0, 2, 1, 2)
        self.iconStatusLabel = QtGui.QLabel(SiteEditor)
        self.iconStatusLabel.setText(_fromUtf8(""))
        self.iconStatusLabel.setObjectName(_fromUtf8("iconStatusLabel"))
        self.gridLayout_2.addWidget(self.iconStatusLabel, 8, 2, 1, 1)
        self.iconLocationLineEdit = QtGui.QLineEdit(SiteEditor)
        self.iconLocationLineEdit.setObjectName(_fromUtf8("iconLocationLineEdit"))
        self.gridLayout_2.addWidget(self.iconLocationLineEdit, 6, 2, 1, 1)
        self.urlLineEdit = QtGui.QLineEdit(SiteEditor)
        self.urlLineEdit.setObjectName(_fromUtf8("urlLineEdit"))
        self.gridLayout_2.addWidget(self.urlLineEdit, 1, 2, 1, 2)
        self.label_4 = QtGui.QLabel(SiteEditor)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 6, 0, 1, 1)
        self.label_2 = QtGui.QLabel(SiteEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtGui.QLabel(SiteEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(SiteEditor)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 2, 2, 1, 2)
        self.iconPreviewLabel = QtGui.QLabel(SiteEditor)
        self.iconPreviewLabel.setText(_fromUtf8(""))
        self.iconPreviewLabel.setObjectName(_fromUtf8("iconPreviewLabel"))
        self.gridLayout_2.addWidget(self.iconPreviewLabel, 9, 2, 1, 1)
        self.checkBoxBrowserPlugins = QtGui.QCheckBox(SiteEditor)
        self.checkBoxBrowserPlugins.setObjectName(_fromUtf8("checkBoxBrowserPlugins"))
        self.gridLayout_2.addWidget(self.checkBoxBrowserPlugins, 5, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.newButtonBox = QtGui.QDialogButtonBox(SiteEditor)
        self.newButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Discard|QtGui.QDialogButtonBox.Save)
        self.newButtonBox.setObjectName(_fromUtf8("newButtonBox"))
        self.gridLayout.addWidget(self.newButtonBox, 2, 0, 1, 1)
        self.existingButtonBox = QtGui.QDialogButtonBox(SiteEditor)
        self.existingButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.existingButtonBox.setObjectName(_fromUtf8("existingButtonBox"))
        self.gridLayout.addWidget(self.existingButtonBox, 3, 0, 1, 1)

        self.retranslateUi(SiteEditor)
        QtCore.QMetaObject.connectSlotsByName(SiteEditor)
        SiteEditor.setTabOrder(self.nameLineEdit, self.urlLineEdit)
        SiteEditor.setTabOrder(self.urlLineEdit, self.iconLocationLineEdit)
        SiteEditor.setTabOrder(self.iconLocationLineEdit, self.browseButton)
        SiteEditor.setTabOrder(self.browseButton, self.newButtonBox)
        SiteEditor.setTabOrder(self.newButtonBox, self.existingButtonBox)

    def retranslateUi(self, SiteEditor):
        SiteEditor.setWindowTitle(QtGui.QApplication.translate("SiteEditor", "Edit Web App", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(QtGui.QApplication.translate("SiteEditor", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SiteEditor", "Icon", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SiteEditor", "URL", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SiteEditor", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SiteEditor", "URL is opened when the web app is launched. Links which do not begin with this URL are opened in a web browser.", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxBrowserPlugins.setText(QtGui.QApplication.translate("SiteEditor", "Enable browser plugins", None, QtGui.QApplication.UnicodeUTF8))

