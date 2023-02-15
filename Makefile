.PHONY: all clean lint type test test-cov

CMD:=
PYMODULE:=helpdesk
MANAGEPY:=$(CMD) ./$(PYMODULE)/manage.py
APPS:=helpdesk accounts teams tickets
SPHINX_ARGS:=docs/ docs/_build -nWE

all: type test check lint

lint: 
	$(CMD) ruff check $(PYMODULE)

lint-fix: 
	$(CMD) ruff check --fix $(PYMODULE)

check:
	$(MANAGEPY) check

dev:
	$(MANAGEPY) runserver

type: 
	cd helpdesk && mypy $(APPS)

test: | $(PYMODULE)
	cd helpdesk && DJANGO_SETTINGS_MODULE=helpdesk.settings pytest --cov=. $(APPS) $(PYMODULE)

test-cov:
	cd helpdesk && DJANGO_SETTINGS_MODULE=helpdesk.settings pytest --cov=. $(APPS) $(PYMODULE) --cov-report html

clean:
	git clean -Xdf # Delete all files in .gitignore
