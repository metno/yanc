simple:
	python tests/test.py
	python3 tests/test.py

test:
	nosetests
	nosetests3

coverage:
	nosetests --with-coverage --cover-erase --cover-package=yanc --cover-html

lint:
	python tests/pep8_test.py

count:
	@wc -l *.py */*.py */*.yml */*/*.yml | tail -1
