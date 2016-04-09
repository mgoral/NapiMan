EXECUTABLE=napiman

####################################################################################################
## Paths
##

PREFIX=${HOME}/.local

####################################################################################################
## Important commands
##

CD = cd
RM = rm -f
MKDIR = mkdir -p
INSTALL ?= install
GEN = tools/gen-in
VIRTUALENV = virtualenv

####################################################################################################
## Other settings
##

# Python version to be used
PYTHON_VER = python3
