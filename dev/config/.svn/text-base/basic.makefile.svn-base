SHELL = /bin/zsh

TARGET_SHARED_LIB :=
TARGET_STATIC_LIB :=
TARGET_EXES       :=
CPP_EXES          := 
C_EXES            := 
FOR_EXES          := 

PROJ_DIR = .
PROJ_NAME := $(shell basename $(PWD))
# BUILD_CONFIG is a variable to distinguish different settings of make,
# like target architecture, compiler version, some package version etc.
# For example, different ROOT versions or gcc versions are not compatible to
# each other. We want to keep the binary files created in separete directories
# such that we don't have to recompile and replace them every time we switch
# from one to another.
# Introduced on 01/07/2006.
BUILD_CONFIG = 

HOST_NAME=$(shell hostname -d)

#--------------------------------------------------------------------
# Old version of the include path for the project. 
# In order to use this old version, overwrite INCDIR in mydep.makefile
# of your project.
# INCDIR = $(PROJ_DIR)/inc
#--------------------------------------------------------------------
#temp := $(shell basename `pwd`)
PROJINCDIR = $(PROJ_DIR)/$(PROJ_NAME)
# INCDIR = $(PROJINCDIR)
INCDIR = $(PROJ_DIR)
SRCDIR = $(PROJ_DIR)/src
OBJDIR = $(PROJ_DIR)/obj
LIBDIR = $(PROJ_DIR)/lib
EXEDIR = $(PROJ_DIR)/exe

ifneq ($(strip $(BUILD_CONFIG)),)
  OBJDIR = $(PROJ_DIR)/obj/$(BUILD_CONFIG)
  $(shell mkdir -p $(OBJDIR))
  LIBDIR = $(PROJ_DIR)/lib/$(BUILD_CONFIG)
  $(shell mkdir -p $(LIBDIR))
  EXEDIR = $(PROJ_DIR)/exe/$(BUILD_CONFIG)
  $(shell mkdir -p $(EXEDIR))
endif

vpath %.hxx $(INCDIR)
vpath %.hpp $(INCDIR)
vpath %.hh $(INCDIR)
vpath %.H $(INCDIR)
vpath %.h $(INCDIR)
vpath %.inc $(INCDIR)

vpath %.cpp $(SRCDIR)
vpath %.cxx $(SRCDIR) $(SRCDIR)/main $(EXTRA_SRCDIRS)
vpath %.cc $(SRCDIR)
vpath %.C $(SRCDIR)
vpath %.c $(SRCDIR)
vpath %.f $(SRCDIR)
vpath %.for $(SRCDIR)
vpath %.fpp $(SRCDIR)
vpath %.java $(SRCDIR)
vpath %Dict.h $(SRCDIR)

vpath %.$(ObjSuf) $(OBJDIR)

vpath %.class $(LIBDIR)
VPATH2 = $(OBJDIR):$(SRCDIR):$(INCDIR):$(LIBDIR):$(EXEDIR):.
ifneq ($(EXTRA_SRCDIRS),"")
  VPATH = $(VPATH2):$(EXTRA_SRCDIRS)
else
  VPATH = $(VPATH2)
endif

ifeq ($(TK_INSTALL_DIR),)
  TK_INSTALL_DIR = $(TK_ROOT)
endif
TK_INCDIR      = $(TK_INSTALL_DIR)/include
TK_LIBDIR      = $(TK_INSTALL_DIR)/lib
TK_BINDIR      = $(TK_INSTALL_DIR)/bin
TK_EXEDIR      = $(TK_BINDIR)
TK_PYTHONDIR   = $(TK_INSTALL_DIR)/python

ifneq ($(strip $(BUILD_CONFIG)),)
  TK_LIBDIR = $(TK_INSTALL_DIR)/lib/$(BUILD_CONFIG)
  $(shell mkdir -p $(TK_LIBDIR))
  TK_BINDIR = $(TK_INSTALL_DIR)/bin/$(BUILD_CONFIG)
  $(shell mkdir -p $(TK_BINDIR))
endif

CppSrcSuf = cxx cpp C cc
CppIncSuf = hxx hpp H hh
ObjSuf    = o
LibSuf    = so
CSrcSuf   = c
CIncSuf   = h
FSrcSuf   = f fpp F

CC            = gcc
CFLAGS        = -O
CXX = g++
CXXFLAGS = -Wall -O -I$(INCDIR)
CFLAGS = -O -I$(INCDIR)
FFLAGS = -O -I$(INCDIR)
INCFLAGS = -I$(INCDIR)
LD = g++
LDFLAGS = -O
SOFLAGS = -shared
LIBS = -L$(TK_ROOT)/lib
SWIG = swig
F77 = gfortran

OBJS    = $(C_OBJS) $(CPP_OBJS) $(FOR_OBJS)


default: all

.PHONY: clean cleanall cleanobj cleanlib cleanbak cleandict
.PHONY: all install default prerequistes
.PHONY: arxiv html

# INCS := $(shell ls $(INCDIR))
# SRCS := $(shell ls $(SRCDIR))

print_basic:

html: $(INCS) $(SRCS)
	root -b -n -l -q makehtml.C

arxiv: cleanbak
	@echo "..... Making an archive of the source files."
	@(set dirname=`pwd`; \
	rm -f $${dirname:t}.tar.gz; \
	gtar cf - Makefile dependencies.makefile my.makefile inc src | \
	gzip - > $${dirname:t}.tgz)
	@echo "`ls -1 *.tgz` has been created"

clean: cleanall

cleanall: cleanobj cleanlib cleandict cleanbak cleanexe \
	clean_custom
	@touch coredummy; rm -f core*

cleandict: 
	@touch $(SRCDIR)/dummyDictdummy; rm -f $(SRCDIR)/*Dict*

cleanobj:
	@if [[ -d $(OBJDIR) ]]; then touch $(OBJDIR)/dummy.o; rm -f $(OBJDIR)/*.o; fi
	@if [[ -d swig ]]; then (touch swig/dummy.o; rm -f swig/*.o); fi

cleanlib:
	@if [[ -d $(LIBDIR) ]]; then \
touch $(LIBDIR)/libdummy.so; touch $(LIBDIR)/libdummy.a; \
rm -f $(LIBDIR)/lib*.so $(LIBDIR)/lib*.a; \
fi

cleanexe: 
	@mkdir -p $(EXEDIR)
	@touch $(EXEDIR)/dummy.exe
	@rm -f $(EXEDIR)/*.exe

cleanbak:
	@touch $(PROJINCDIR)/dummy~;
	@touch $(SRCDIR)/dummy~;
	@if [[ -d $(OBJDIR) ]]; then touch $(OBJDIR)/dummy~; rm $(OBJDIR)/*~; fi
	@touch dummy~;
	@rm -f $(PROJINCDIR)/*~ $(SRCDIR)/*~ *~ 

clean_custom:
	@if [[ -e ./scripts/clean.sh ]]; then ./scripts/clean.sh; fi

include $(TKDEV_ROOT)/config/tools.makefile
