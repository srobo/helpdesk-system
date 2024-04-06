.PHONY: all clean format format-check lint type test test-cov

CMD:=
PYMODULE:=helpdesk
MANAGEPY:=$(CMD) ./$(PYMODULE)/manage.py
APPS:=helpdesk accounts display teams tickets
SPHINX_ARGS:=docs/ docs/_build -nWE

all: type test format lint

format:
	find $(PYMODULE) -name "*.html" | xargs $(CMD) djhtml
	$(CMD) ruff format $(PYMODULE)

format-check:
	find $(PYMODULE) -name "*.html" | xargs $(CMD) djhtml --check
	$(CMD) ruff format --check $(PYMODULE)

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
