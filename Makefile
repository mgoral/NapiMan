include config.mk

####################################################################################################
## Directories
##

BUILD_DIR = build
SRC_DIR = nm

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

INSTALL_PATH=$(DESTDIR)$(prefix)
VENV_DIR = $(INSTALL_PATH)/share/napiman/venv

GEN = NAPIMAN_VENV_DIR=$(VENV_DIR) tools/gen-in

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
	$(RM) -rf "$(INSTALL_PATH)/share/napiman"

.PHONY: clean
clean:
	$(RM) -r "$(BUILD_DIR)"
	$(RM) "$(GEN_FILES)"

.PHONY: bootstrap
bootstrap: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: requirements.txt
	@test -d $(VENV_DIR) || $(VIRTUALENV) --python="$(PYTHON_VER)" "$(VENV_DIR)"
	@$(VENV_DIR)/bin/pip install -Ur $<
	@touch $(VENV_DIR)/bin/activate

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
