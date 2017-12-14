#
# (1) C_OBJS, CPP_OBJS and FOR_OBJS to contain .o files to be created from
#     c(.c), c++(.cxx, .cpp, .cc, .C) or fortran(.f, .fpp) source files.
#     These OBJS variables contain only .o files to be linked to create
#     a library or an executable file, i.e. .o files containing the main
#     program are excluded. 
# (2) .o files for main programs must be set by the user in the mydep.makefile
#     by specifying CPP_EXES(.exe), C_EXES(.exe), FOR_EXES(.exe). By specifying
#     these variables, .o files for these files will be automatically 
#     excluded in OBJS files mentioned in (1).
# (3) 

srcdirs = $(SRCDIR) $(EXTRA_SRCDIRS)

CPP_EXES    := 
C_EXES      := 
F_EXES    := 
C_MAIN_OBJS = $(patsubst %.exe,%.$(ObjSuf), $(C_EXES))
CPP_MAIN_OBJS = $(patsubst %.exe,%.$(ObjSuf), $(CPP_EXES))
F_MAIN_OBJS = $(patsubst %.exe,%.$(ObjSuf), $(F_EXES))
MAIN_OBJS   := $(CPP_MAIN_OBJS) $(C_MAIN_OBJS) $(F_MAIN_OBJS)

C_OBJS      = $(foreach dir, $(srcdirs), \
		$(patsubst $(dir)/%.$(CSrcSuf),%.$(ObjSuf), \
		$(foreach suf, $(CSrcSuf), \
		$(wildcard $(dir)/*.$(suf)))))
C_LIB_OBJS      = $(filter-out $(C_MAIN_OBJS), $(C_OBJS))
include $(CONFIG_DIR)/rpc.makefile
C_LIB_OBJS2     = $(addprefix $(OBJDIR)/, $(C_LIB_OBJS))

CPP_OBJS  = $(foreach dir, $(srcdirs), \
		$(filter-out $(DICTOBJS),\
		$(addsuffix .$(ObjSuf), $(basename $(patsubst $(dir)/%, %, \
		$(foreach suf, $(CppSrcSuf), $(wildcard $(dir)/*.$(suf)))) \
		))))
CPP_LIB_OBJS     = $(filter-out $(CPP_MAIN_OBJS), $(CPP_OBJS))
CPP_LIB_OBJS2    = $(addprefix $(OBJDIR)/, $(CPP_LIB_OBJS))

# Fortran OBJS
F_OBJS      = $(foreach dir, $(srcdirs), $(addsuffix .$(ObjSuf), $(basename \
		$(patsubst $(dir)/%,%, \
		$(foreach suf, $(FSrcSuf), \
		$(wildcard $(dir)/*.$(suf)))))))
F_LIB_OBJS      = $(filter-out $(F_MAIN_OBJS),$(F_OBJS))
F_LIB_OBJS2     = $(addprefix $(OBJDIR)/, $(F_LIB_OBJS))

# JAVA classes
JAVA_CLASSES  = $(patsubst $(SRCDIR)/%.java,%.class, \
		$(wildcard $(SRCDIR)/*.java))

LIB_OBJS      = $(CPP_LIB_OBJS) $(DICTOBJS) $(C_LIB_OBJS) $(F_LIB_OBJS)
LIB_OBJS2     = $(addprefix $(OBJDIR)/, $(LIB_OBJS))

#----------------------------------------------------------------
# ROOT dictionaries
#----------------------------------------------------------------
# Old way using CINT
#DICTSRCSLINKDEF = $(patsubst $(PROJINCDIR)/%LinkDef.hxx, $(SRCDIR)/%Dict.cxx, \
#		$(wildcard $(PROJINCDIR)/*LinkDef.hxx))

#DICTOBJS  += $(patsubst $(SRCDIR)/%.cxx,%.$(ObjSuf), $(DICTSRCSLINKDEF))
#DICTOBJS2 += $(addprefix $(OBJDIR)/, $(DICTOBJS))

# New way of generating ROOT dictionaries using Reflex
ROOTDICT_HEADERS = 
ROOTDICT_LINKDEF = 
ROOTDICTHDRS = $(foreach suf, h hxx, \
	$(patsubst %.$(suf),../$(PROJINCDIR)/%.$(suf), \
	$(filter %.$(suf), $(ROOTDICT_HEADERS))))
ROOTDICTSRCS = $(patsubst %LinkDef.hxx,$(SRCDIR)/%Dict.cxx, \
		$(ROOTDICT_LINKDEF))
DICTOBJS  += $(patsubst $(SRCDIR)/%.cxx,%.$(ObjSuf), $(ROOTDICTSRCS))
DICTOBJS2 += $(addprefix $(OBJDIR)/, $(DICTOBJS))

#----------------------------------------------------------------
# SWIG
#----------------------------------------------------------------
# Requires SWIG_MODULE, SWIG_I to be specified
SWIG_CPP = $(addsuffix .cxx, $(SWIG_MODULE))
SWIG_OBJS = $(addsuffix .o, $(SWIG_MODULE))
SWIG_LIB = $(patsubst swig/%,swig/_%.so, $(SWIG_MODULE))

all: 


#install: all
#	@echo "Installing header files to $(TK_INCDIR) ..."
#	@cp inc/*.* $(TK_INCDIR)/
#	@echo "Installing library files to $(TK_LIBDIR) ..."
#	@cp lib/lib*.* $(TK_LIBDIR)/
