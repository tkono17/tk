#
# RPC 
#
vpath %.x $(INCDIR)

RPC_DEF_FILES = $(patsubst $(INCDIR)/%,%, $(wildcard $(INCDIR)/*.x))

RPC_C_FILES = $(patsubst %.x,$(SRCDIR)/%_xdr.c, $(RPC_DEF_FILES))
RPC_O_FILES = $(addsuffix _xdr.o, $(basename $(RPC_DEF_FILES)))
TMP := $(filter %_xdr.o, $(C_LIB_OBJS))
TMP := $(filter-out $(TMP), $(RPC_O_FILES))
C_LIB_OBJS += $(TMP)

$(RPC_C_FILES): $(SRCDIR)/%_xdr.c: %.x
	(cd $(INCDIR); rpcgen $(<F))
	mv $(INCDIR)/$(@F) $(SRCDIR)

