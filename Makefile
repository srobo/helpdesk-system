.PHONY: all clean lint type test test-cov

CMD:=
PYMODULE:=helpdesk
MANAGEPY:=$(CMD) ./$(PYMODULE)/manage.py
APPS:=helpdesk
SPHINX_ARGS:=docs/ docs/_build -nWE

all: type test check lint

lint: 
	$(CMD) flake8 $(PYMODULE) $(TESTS)

check:
	$(MANAGEPY) check

dev:
	$(MANAGEPY) runserver

type: 
	cd helpdesk && mypy $(APPS)

test: | $(PYMODULE)
	cd helpdesk && pytest --cov=. $(APPS) $(PYMODULE)

test-cov:
	cd helpdesk && pytest --cov=. $(APPS) $(PYMODULE) --cov-report html

isort:
	$(CMD) isort $(PYMODULE) $(TESTS)

clean:
	git clean -Xdf # Delete all files in .gitignore