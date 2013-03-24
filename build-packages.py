from glob import glob
import os

from py2deb import Py2deb

version = '1.1.0'

os.system('make py')

p = Py2deb("webplier")
p.author = "Ken Kinder"
p.mail = "kkinder@gmail.com"
p.description = "Webplier creates site-specific browsers, also called web apps, for your Linux desktop. Each web app " \
                "has its own taskbar, launcher, and menu entry, along with its own cookie jar, user scripts, and preferences."
p.url = "http://webplier.com"
p.depends = "python2.7, python-qt4, python-xdg"
p.license = "gpl"
p.section = "web"
p.arch = "all"

p["/usr/share/applications"] = ["webplier/webplier.desktop|webplier.desktop"]
p["/usr/share/icons"] = ["webplier/resources/webplier.png|webplier.png"]
p["/usr/bin"] = ["plier"]
p["/usr/lib/python2.7/dist-packages"] = ["Webplier-1.1.0.egg-info"]
p['/usr/lib/python2.7/dist-packages/webplier'] = map(lambda x: '%s|%s' % (x, x.split('/')[-1]), glob("webplier/*.py") + glob("webplier/*.pyc") + \
                                        glob("webplier/*.html") + ['webplier/ABOUT', 'webplier/COPYING',
                                                                   'webplier/VERSION', 'webplier/ICONS'])
p['/usr/lib/python2.7/dist-packages/webplier/ui'] = map(lambda x: '%s|%s' % (x, x.split('/')[-1]), glob("webplier/ui/*"))

p.generate(version, rpm=True, src=True)
