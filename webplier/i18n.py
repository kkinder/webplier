from PyQt4.QtCore import QCoreApplication, QString
import os

tr = QCoreApplication.translate

try:
    fromUtf8 = QString.fromUtf8
except AttributeError:
    fromUtf8 = lambda s: s

APP_NAME, VERSION, DATE = open(os.path.join(os.path.dirname(__file__), 'VERSION')).read().split('\n', 3)
ABOUT_TEXT = open(os.path.join(os.path.dirname(__file__), 'ABOUT')).read().decode('utf8')

__all__ = ['tr', 'fromUtf8', APP_NAME, VERSION, DATE    ]
