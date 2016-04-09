EXECUTABLE=napiman

####################################################################################################
## Paths
##

PREFIX=${HOME}/.local

####################################################################################################
## Directories
##

BUILD_DIR = build
SRC_DIR = nm

####################################################################################################
## Important commands
##

CD = cd
RM = rm -f
MKDIR = mkdir -p
INSTALL?=install
GEN=tools/gen-in
VIRTUALENV = virtualenv

####################################################################################################
## Other settings
##

# Python version to be used
PYTHON_VER = python3
