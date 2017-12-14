BOOST_DIR := /usr
#BOOST_DIR := 

# Set BOOST install directory according to the host
HOST_NAME=$(shell hostname -d)

ifeq ($(HOST_NAME), naf.desy.de)
BOOST_DIR := /scratch/hh/lustre/atlas/users/tkohno/local
BOOST_VERSION := 1.43.0
endif

ifeq ($(HOST_NAME), desy.de)
endif

ifeq ($(HOST_NAME),cern.ch)
endif

INC_APPEND=
EXTRA_LIBDIR=
ifeq ($(HOST_NAME),icepp.jp)
BOOST_DIR := $(BoostDir)
BOOST_VERSION := 1.53.0
INC_APPEND=/boost-1_53
EXTRA_LIBDIR=$(workdir)/local/lib
endif

#ifneq ($(BOOST_DIR), /usr)
#CXXFLAGS += -I$(BOOST_DIR)/include
#INCFLAGS += -I$(BOOST_DIR)/include
#LIBS += -L$(BOOST_DIR)/lib
#endif

ifneq ($(BOOST_DIR), )
CXXFLAGS += -I$(BOOST_DIR)/include$(INC_APPEND)
INCFLAGS += -I$(BOOST_DIR)/include$(INC_APPEND)
LIBS += -L$(BOOST_DIR)/lib
endif

ifneq ($(EXTRA_LIBDIR), )
LIBS += -L$(EXTRA_LIBDIR)
endif

