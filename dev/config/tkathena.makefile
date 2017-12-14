TKATHENA_DIR = $(TK_ROOT)
TKATHENA_DIR = /space2/tkohno/athena/13.0.X_analysis/InstallArea
TKATHENA_BINDIR = $(TK_BINDIR)
TKATHENA_EXEDIR = $(TK_BINDIR)
TKATHENA_LIBDIR = $(TKATHENA_DIR)/i686-slc4-gcc34-opt/lib
TKATHENA_INCDIR = -I$(TKATHENA_DIR)/include/RecData \
		-I$(TKATHENA_DIR)/include/TrigData \
		-I$(TKATHENA_DIR)/include/EventData \
		-I$(TKATHENA_DIR)/include/TreeManagers \
		-I$(TKATHENA_DIR)/include/TkUtils

CXXFLAGS += $(TKATHENA_INCDIR)
INCFLAGS += $(TKATHENA_INCDIR)
LIBS     += # -L$(TKATHENA_LIBDIR) -lATREvent -lTreeManagers -lTkUtils

