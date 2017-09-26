test:
	nosetests
	nosetests3

testop:
	python tests/operational.py

coverage:
	nosetests --with-coverage --cover-erase --cover-package=yanc --cover-html

lint:
	python tests/pep8_test.py

count:
	@wc -l *.py */*.py */*.yml */*/*.yml | tail -1
