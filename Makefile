include config.mk


####################################################################################################
## Building executable
##

# Files which need some substitutions
GEN_FILES = nm/version.py

## Created executable options
EXEC_PATH=$(BUILD_DIR)/$(EXECUTABLE)
ZIP_EXCLUDES="*__pycache__*" "*.pyc" "*.in"
ZIP_EXCLUDE_FLAGS=$(foreach e, $(ZIP_EXCLUDES), -x $e)
PYTHON_SOURCES=$(shell find $(SRC_DIR) -type f -name '*.py') \
			   __main__.py

INSTALL_PATH=$(DESTDIR)$(PREFIX)

.PHONY: all
all: $(EXEC_PATH)

.PHONY: install
install: all bootstrap napiman-start
	$(INSTALL) "$(EXEC_PATH)" "$(VENV_DIR)/bin"
	@$(INSTALL) -m 755 -d "$(INSTALL_PATH)/bin"
	$(INSTALL) napiman-start "$(INSTALL_PATH)/bin/napiman"

.PHONY: uninstall
uninstall:
	$(RM) "$(INSTALL_PATH)/bin/$(EXECUTABLE)"
	$(RM) "$(VENV_DIR)/bin/$(EXECUTABLE)"

.PHONY: clean
clean:
	$(RM) -r "$(BUILD_DIR)"
	$(RM) -r "$(VENV_DIR)"
	$(RM) "$(GEN_FILES)"

.PHONY: bootstrap
bootstrap: $(VENV_DIR)

$(VENV_DIR):
	@$(VIRTUALENV) --python="$(PYTHON_VER)" "$(VENV_DIR)"
	@. $(VENV_DIR)/bin/activate && pip install -r requirements.txt

$(EXEC_PATH): $(EXEC_PATH).zip
	@$(RM) "$@"
	@echo '#!/usr/bin/env $(PYTHON_VER)' | cat - "$<" > "$@"
	@chmod +x "$@"
	@echo "Created $(BUILD_DIR)/$(EXECUTABLE)"

$(EXEC_PATH).zip: $(GEN_FILES) $(PYTHON_SOURCES)
	@$(MKDIR) "$(BUILD_DIR)"
	@$(RM) "$@"
	@zip --quiet $(ZIP_EXCLUDE_FLAGS) -r "$@" $^

%.py: %.py.in
	@echo "Generating: $< -> $@"
	@$(GEN) "$<" > "$@"

napiman-start: napiman-start.in
	@echo "Generating: $< -> $@"
	@$(GEN) "$<" > "$@"
