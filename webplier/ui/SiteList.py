# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SiteList.ui'
#
# Created: Wed Feb 27 22:47:10 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SiteList(object):
    def setupUi(self, SiteList):
        SiteList.setObjectName(_fromUtf8("SiteList"))
        SiteList.resize(914, 527)
        self.gridLayout = QtGui.QGridLayout(SiteList)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.siteListWidget = QtGui.QListWidget(SiteList)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.siteListWidget.sizePolicy().hasHeightForWidth())
        self.siteListWidget.setSizePolicy(sizePolicy)
        self.siteListWidget.setObjectName(_fromUtf8("siteListWidget"))
        self.verticalLayout.addWidget(self.siteListWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.addButton = QtGui.QPushButton(SiteList)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(SiteList)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.horizontalLayout.addWidget(self.removeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.siteEditorWidget = QtGui.QWidget(SiteList)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.siteEditorWidget.sizePolicy().hasHeightForWidth())
        self.siteEditorWidget.setSizePolicy(sizePolicy)
        self.siteEditorWidget.setObjectName(_fromUtf8("siteEditorWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.siteEditorWidget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_3.addWidget(self.siteEditorWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.aboutButton = QtGui.QPushButton(SiteList)
        self.aboutButton.setObjectName(_fromUtf8("aboutButton"))
        self.horizontalLayout_2.addWidget(self.aboutButton)
        self.closeButton = QtGui.QPushButton(SiteList)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
        self.closeButton.setSizePolicy(sizePolicy)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)

        self.retranslateUi(SiteList)
        QtCore.QMetaObject.connectSlotsByName(SiteList)

    def retranslateUi(self, SiteList):
        SiteList.setWindowTitle(QtGui.QApplication.translate("SiteList", "Webplier - Site List", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("SiteList", "Add Site", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("SiteList", "Remove Site", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutButton.setText(QtGui.QApplication.translate("SiteList", "About Webplier", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("SiteList", "Close", None, QtGui.QApplication.UnicodeUTF8))

