test:
	nosetests

testop:
	python yanc/tests/operational.py

coverage:
	nosetests --with-coverage --cover-erase --cover-package=yanc --cover-html

lint:
	flake8 --inore=E501

count:
	@wc -l *.py */*.py */*.yml */*/*.yml | tail -1
