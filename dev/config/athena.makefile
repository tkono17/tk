define addCmtIncludes
# $(1) cmt_project_path
# $(2) list of packages
CXXFLAGS += $(addprefix -I$(1)/InstallArea/include/, $(2))
INCFLAGS += $(addprefix -I$(1)/InstallArea/include/, $(2))
endef

define addCmtPackage
# $(1) cmt package name (will use cmt macros $(1)_home and $(1)_linkopts)
# $(2) A cmt directory to invoke cmt commands
$(1)_home := $(shell cd $(2); cmt show macro_value $(1)_home)
CXXFLAGS += -I$$(value $(1)_home)/include
INCFLAGS += -I$$(value $(1)_home)/include
LIBS     += $(shell cd $(2); cmt show macro_value $(1)_linkopts)
endef

define addCmtPackages
# $(1) cmt_project_path
# $(2) list of packages
CXXFLAGS += $(addprefix -I$(1)/InstallArea/include/, $(2))
INCFLAGS += $(addprefix -I$(1)/InstallArea/include/, $(2))
LIBS     += -L$(1)/InstallArea/$(CMTCONFIG)/lib $$(addprefix -l, $(2))
endef

