EXECUTABLE=napiman

####################################################################################################
## Paths
##

# Lower case on purpose so user can type a standard `make install prefix=/usr`
prefix = ${HOME}/.local

####################################################################################################
## Important commands
##

CD = cd
RM = rm -f
MKDIR = mkdir -p
INSTALL ?= install
VIRTUALENV = virtualenv

####################################################################################################
## Other settings
##

# Python version to be used
PYTHON_VER = python3
