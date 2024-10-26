DIR_VENV		:=	venv

CMD_BLACK		:=	$(DIR_VENV)/bin/black
CMD_ISORT		:=	$(DIR_VENV)/bin/isort
CMD_MYPY		:=	$(DIR_VENV)/bin/mypy
CMD_PIP			:=	$(DIR_VENV)/bin/pip3
CMD_PY			:=	$(DIR_VENV)/bin/python3
CMD_PYLINT		:=	$(DIR_VENV)/bin/pylint

SCR_MAIN		:=	dataspass.py


.PHONY: help
help:
	@echo "+-----------+"
	@echo "| dataspass |"
	@echo "+-----------+"
	@echo
	@echo "venv                 prepare virtual environment"
	@echo "requirements-dev     install dev requirements"
	@echo
	@echo "black                run black"
	@echo "isort                run isort"
	@echo "mypy                 run mypy"
	@echo "pylint               run pylint"
	@echo



$(DIR_VENV):
	python3 -m venv "$(DIR_VENV)"
	$(CMD_PIP) install -U pip

$(CMD_BLACK) $(CMD_ISORT) $(CMD_MYPY) $(CMD_PYLINT): | $(DIR_VENV)
	$(CMD_PIP) install -r requirements-dev.txt

.PHONY: requirements-dev
requirements-dev: $(CMD_BLACK) $(CMD_ISORT) $(CMD_MYPY) $(CMD_PYLINT)



define _black
	$(CMD_BLACK) \
		--line-length=79 \
		$(1)
endef

.PHONY: black
black: $(CMD_BLACK)
	$(call _black,$(SCR_MAIN))



define _isort
	$(CMD_ISORT) \
		--settings-file ".isort.cfg" \
			$(1)
endef

.PHONY: isort
isort: $(CMD_ISORT)
	$(call _isort,$(SCR_MAIN))



define _mypy
	$(CMD_MYPY) \
		--config-file ".mypy.ini" \
			$(1)
endef

.PHONY: mypy
mypy: $(CMD_MYPY)
	$(call _mypy,$(SCR_MAIN))



define PYLINT_MESSAGE_TEMPLATE
{C} {path}:{line}:{column} - {msg}
  ↪  {category} {module}.{obj} ({symbol} {msg_id})
endef
export PYLINT_MESSAGE_TEMPLATE

define _pylint
	$(CMD_PYLINT) \
		--disable "C0111" \
		--disable "R0801" \
		--msg-template="$$PYLINT_MESSAGE_TEMPLATE" \
		--output-format="colorized" \
			$(1)
endef

.PHONY: pylint
pylint: $(CMD_PYLINT)
	$(call _pylint,$(SCR_MAIN))



.PHONY: action
action: black isort mypy pylint
