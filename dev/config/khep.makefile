KHEP_DIR = $(TK_INSTALL_DIR)
KHEP_BINDIR = $(TK_BINDIR)
KHEP_EXEDIR = $(TK_BINDIR)
KHEP_LIBDIR = $(KHEP_DIR)/lib
KHEP_INCDIR = -I$(KHEP_DIR)/include/KHepBase -I$(KHEP_DIR)/include/KHepRoot -I$(KHEP_DIR)/include/KHepUtil

CXXFLAGS += $(KHEP_INCDIR)
INCFLAGS += $(KHEP_INCDIR)
LIBS     += # -L$(KHEP_LIBDIR) -lKHepBase -lKHepRoot -lKHepUtil