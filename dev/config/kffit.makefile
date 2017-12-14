#
#
#
KFFIT_DEV_DIR = $(ZSOFT_ROOT)/zeus/recon/Phase2/kfrecon/v2003a.1
# KFFIT_INC_DIR = $(ZSOFT_ROOT)/zeus/recon/Phase2/kfrecon/v2003a.1/inc
# KFFIT_DEV_DIR = /tokyo/raid3/kohno/mvd/programs/kfrecon
KFFIT_INC_DIR = /tokyo/raid3/kohno/mvd/programs/kfrecon/inc
CXXFLAGS += -I$(KFFIT_INC_DIR)/mvd -I$(KFFIT_INC_DIR)/util
INCFLAGS += -I$(KFFIT_INC_DIR)/mvd -I$(KFFIT_INC_DIR)/util
