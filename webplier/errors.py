"""
For dealing with errors.
"""
import sys

from PyQt4.QtGui import QMessageBox, QWidget

app = None


def showError(title, message):
    if app:
        QMessageBox.critical(QWidget(), title, message, QMessageBox.Ok)
    else:
        print >> sys.stderr, title
        print >> sys.stderr, message
