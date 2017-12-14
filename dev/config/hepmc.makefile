HEPMC_DIR :=

# Set HepMC install directory according to the host
ifeq ($(HOST_NAME), naf.desy.de)
HEPMC_DIR := /scratch/hh/lustre/atlas/users/tkohno/local
HEPMC_VERSION := 
endif
ifeq ($(HOST_NAME), desy.de)
endif
ifeq ($(HOST_NAME),cern.ch)
endif

ifneq ($(HEPMC_DIR), )
CXXFLAGS += -I$(HEPMC_DIR)/include
LIBS += -L$(HEPMC_DIR)/lib -lHepMC
INCFLAGS += -I$(HEPMC_DIR)/include
endif

