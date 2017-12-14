#--------------------------------------------------------------------------
# Follow packages dependencies (DEPENDS_ON) and update the configuration
#--------------------------------------------------------------------------
extra_packages = 

define add_package
  # $$(info Update configuration from $(1))
  make_fragment = $(ProjectDir)/dev/$(1)/mydep.makefile
  status = $$(shell ls $$(make_fragment))
  ifeq ($$(status),$$(make_fragment))
    include $$(make_fragment)
  else
    $$(warn $$(make_fragment) not found)
  endif
endef

$(foreach package,$(DEPENDS_ON), \
	$(eval $(call add_package,$(package)) ) )

