#---------------------------------------------------------------------
# KZLIB related stuffs
#---------------------------------------------------------------------
KZLIB_DIR = $(TK_INSTALL_DIR)
KZLIB_BINDIR = $(KZLIB_DIR)/bin
KZLIB_EXEDIR = $(KZLIB_BINDIR)
KZLIB_LIBDIR = $(KZLIB_DIR)/lib
KZLIB_INCDIR = $(KZLIB_DIR)/include/KZlib

CXXFLAGS += -I$(KZLIB_INCDIR)
INCFLAGS += -I$(KZLIB_INCDIR)
# LIBS     += -L$(KZLIB_LIBDIR)

#
KZLIBS = -L$(KZLIB_LIBDIR) -lKZUtil -lKZBase -lKZCut -lKZAnal
CXXFLAGS += -I$(KZLIB_INCDIR)/KZFortran/structs
CXXFLAGS += -I$(KZLIB_INCDIR)/KZFortran
#
