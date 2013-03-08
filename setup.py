#!/usr/bin/env python2.7

from distutils.core import setup

setup(name='Webplier',
      version='1.0.1',
      description='Webplier creates site-specific browsers, also called web apps, for your Linux desktop.',
      author='Ken Kinder',
      author_email='kkinder@gmail.com',
      url='http://webplier.com/',
      download_url='http://webplier.com/download/',
      packages=['webplier', 'webplier.ui'],
      scripts=['plier'],
      package_data={'webplier': ['ICONS', 'COPYING', 'ICONS.html', 'COPYING.html', 'ABOUT', 'VERSION']},
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: X11 Applications :: Qt',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Browsers',
          'Topic :: Utilities'
      ],
      data_files=[('/usr/share/applications', ["webplier/webplier.desktop"]),
                  ('/usr/share/icons', ['webplier/resources/webplier.png']),
                  ],
)
