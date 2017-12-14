ROOTCFLAGS := $(shell root-config --cflags)
ROOTLIBS   := $(shell root-config --libs)
ROOTGLIBS  := $(shell root-config --glibs)

# Hacks to solve the problem on atlas.naf.desy.de with athena environment
#_root_path = $(shell dirname $(shell which root))
#ROOTCFLAGS = $(subst $(PWD)/../../../../../,$(_root_path)/../../../../../, \#
#		$(ROOTCFLAGS0))
#ROOTLIBS = -L$(ROOTSYS)/lib $(wordlist 2,10000, $(ROOTLIBS0))
#ROOTGLIBS = -L$(ROOTSYS)/lib $(wordlist 2,1000, $(ROOTGLIBS0))


ROOT_DIR = $(TK_INSTALL_DIR)
ROOT_BINDIR = $(ROOT_DIR)/bin
ROOT_EXEDIR = $(ROOT_BINDIR)
ROOT_INCDIR = $(ROOT_DIR)/include
ROOT_LIBDIR = $(ROOT_DIR)/lib

CXXFLAGS += $(ROOTCFLAGS)
additional_ROOT_libs := -lMinuit # -lCintex -lReflex (problem with 5.26.00)
LIBS     += $(ROOTGLIBS) $(additional_ROOT_libs)
GLIBS    += $(ROOTGLIBS) $(additional_ROOT_libs)

INCFLAGS += $(ROOTCFLAGS)
