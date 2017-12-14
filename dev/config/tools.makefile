#-----------------------------------------------------------------------
# Tools to configure Makefile
#-----------------------------------------------------------------------

define gen_use_package
$(eval fragment=$(TKDEV_ROOT)/config/$(1).makefile)
include $(fragment)
endef

#echo $(info a=$(a))
#ifeq $(wildcard $(fragment),) 
#  $(info found $(fragment))
#else
#  $(info not found))
#endif
#endef


define use_package
$(info $(call gen_use_package,$(1)) )
endef

#$(eval $a)
#	
#	$(info fragment is $(fragment))
##$(if $(wildcard $(value fragment)), $(info OK$(fragment)))
##$(if $(wildcard $(value fragment2)), $(info NOT OK$(fragment)))

