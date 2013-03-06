import os

from PyQt4.QtGui import QMessageBox

from i18n import ABOUT_TEXT, VERSION, tr, APP_NAME

COPYING_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'COPYING.html'))
ICONS_FILE =  os.path.abspath(os.path.join(os.path.dirname(__file__), 'ICONS.html'))

title, url, copyright, about = ABOUT_TEXT.split('\n', 3)
ABOUT_HTML = u'<h1>%s</h1>%s<br/><strong>%s</strong><br/>%s<hr/>%s' % (title, VERSION, copyright, url, about)
ABOUT_HTML = ABOUT_HTML.replace(
   u'<http://webplier.com>', u'<a href="http://webplier.com">webplier.com</a>').replace(
   u'\n\n', u'<br/><br/>').replace(
   u'COPYING', u'<a href="file://%s">COPYING</a>' % COPYING_FILE).replace(
   u'ICONS', u'<a href="file://%s">ICONS</a>' % ICONS_FILE)

def show(parent):
    QMessageBox.about(parent, tr('About', 'About %s' % APP_NAME), ABOUT_HTML)
