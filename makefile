.PHONY: dist test

dist:
	# This produces distributions for pypi. The are placed in dist
	python setup.py sdist
	python setup.py bdist_wheel
	@ echo "Run 'twine upload dist/* --verbose'"

test:
	coverage run --source yanc -m unittest discover

coverage:
	nosetests --with-coverage --cover-erase --cover-package=yanc --cover-html

testop:
	# TODO: Update the script after MEPS changed filenames
	python yanc/tests/operational.py

lint:
	python yanc/tests/pep8_test.py

count:
	@wc -l *.py */*.py */*.yml */*/*.yml | tail -1
