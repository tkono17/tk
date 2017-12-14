#clhep_config_exe = clhep-config

#CLHEP_DIR := $(shell $(clhep_config_exe) --prefix)
#CXXFLAGS += $(shell $(clhep_config_exe) --include)
#LIBS += $(shell $(clhep_config_exe) --libs)
#INCFLAGS += $(shell $(clhep_config_exe) --include)

CLHEP_DIR :=

# Set CLHEP install directory according to the host
ifeq ($(HOST_NAME), naf.desy.de)
CLHEP_DIR := /scratch/hh/lustre/atlas/users/tkohno/local
CLHEP_VERSION := 2.0.4.6
endif
ifeq ($(HOST_NAME), desy.de)
CLHEP_DIR := /opt/products/CLHEP/2.0.4.5
CLHEP_VERSION := 2.0.4.5
endif
ifeq ($(HOST_NAME),cern.ch)
CLHEP_DIR := /afs/cern.ch/sw/lcg/external/clhep/1.9.4.4/i686-slc5-gcc43-opt
CLHEP_VERSION := 1.9.4.4
endif

ifneq ($(CLHEP_DIR), )
CXXFLAGS += -I$(CLHEP_DIR)/include
LIBS += -L$(CLHEP_DIR)/lib -lCLHEP-$(CLHEP_VERSION)
INCFLAGS += -I$(CLHEP_DIR)/include
endif

