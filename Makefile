clean:
	find -name "*.pyc" -exec rm "{}" \;
	touch build dist deb_dist
	rm -r build dist deb_dist
	rm *.tar.gz *.deb *.rpm

py:
	python2.7 /usr/lib/python2.7/compileall.py -f .

dist:
	python setup.py sdist
	python setup.py bdist
	python build-packages.py
#	#python setup.py bdist_rpm
#	#python setup.py --command-packages=stdeb.command bdist_deb

