#!/usr/bin/env zsh

function installFile() {
    if [[ ${#*} -ge 2 ]]; then
	src=$1;
	dest=$2;
	cpopt=(${*[3,${#*}]})
	if [[ ! -e $dest || $dest -ot $src ]]; then
	    if [[ ! -e $dest ]]; then echo "no dest"; fi
	    if [[ $dest -ot $src ]]; then echo "dest older"; fi
	    echo "Installing $src to $dest"
	    cp $cpopt $src $dest
	    if [[ $? -ne 0 ]]; then
		echo "Error while: cp $cpopt $src $dest"
	    fi
	fi
    fi
}

scripts=(\
    config/make_dir.sh
    scripts/prep_project.sh
    scripts/prepReactProject.sh
    scripts/initReactWebpack.sh
    scripts/cmd_package.sh
    python/mk_rootLinkDef.py #kill_root.py
    python/mk_tkwt.py
    python/proc_xslt.py
    python/mem_clean.py
    scripts/fig2tex.sh
    scripts/mk_tkweb.sh
    scripts/mk_tex_project.sh 
    scripts/mk_analysis_dir.sh 
    scripts/runRootMacro.py
    scripts/chfn.sh 
    scripts/cp_chname.sh
    scripts/cprm.sh
    scripts/mk_filelist.py
    python/insert_in_tag.py
    #python/jobmgr.py
    scripts/jmgui.py
    scripts/genDatasetMap.py
    scripts/mycron.py
    scripts/make_usePackage.sh
    scripts/mk_html_react.sh

    # LXBATCH tools
    scripts/lxbatch_sub.sh

    # NAF
    scripts/runOnNafBatch.sh
    scripts/list_dcache.sh
    scripts/parse_dcachelist.py

    # ATHENA or CMT utilities
    scripts/ath_install_khep.sh
    scripts/ath_runcmt.sh
    scripts/ath_runMTPT.sh
    scripts/ath_ls_packages.sh
    scripts/ath_make_all.sh
    scripts/ath_cd_project.sh
    scripts/ath_cd_project2.sh
    scripts/ath_get_installarea.sh
    scripts/ath_job_prepare.sh
    scripts/ath_job_run.sh
    scripts/ath_run_trigval.sh
    scripts/ath_chk_nightly.sh
    scripts/ath_atn_test.sh
    scripts/ath_trigCond.py
    scripts/ath_trf.sh
    scripts/ath_rdobs.sh
    scripts/ath_parse_lumicalc.py
    scripts/ath_ami.sh
    scripts/ath_start_ara.sh
    #scripts/ath_lumicalc.py
    scripts/atl_rq.sh
    scripts/atl_grl_ds.py
    scripts/atl_prepare_gridjob.sh
    scripts/atl_dq2freeze.py
    scripts/atl_dq2erase.py
    scripts/atl_lumipsNtuple.sh
    scripts/atl_splitInRuns.py
    scripts/atl_extractRAW.py
    python/athtools/ath_mktar_packages.py 
    python/athtools/ath_jo_insert.py 
    python/athtools/tm_menulist.py
    python/athtools/tm_compxml.py
    python/athtools/trigconf_hltseq.py
    python/trigconf_dumphltchain.py
    scripts/svnWorkTool.sh
    python/mk_sub_grl.py
    scripts/correct_d3pdreader_header.py
    scripts/ath_cmake.sh
    scripts/atlasAnalysisCmake.sh
    scripts/memo_ath_git.sh
    scripts/memo_ath_dev.sh

    # GRID utilities
    scripts/panda_submit.sh
    scripts/panda_submit2.sh
    scripts/ganga_submit.sh
    scripts/ganga_resubmit.sh
    scripts/ganga_status.sh
    scripts/ganga_get.sh
    scripts/ganga_ce_info.sh
    scripts/ganga_ce_with_dataset.sh
    scripts/copyFilesFromGrid.sh
    scripts/grid_delete_datasets.sh
    scripts/grid_chk_missingDS.sh
    atlas/grid/atg_mk_filelist.sh
    atlas/grid/lcgjob.py
    atlas/grid/setup_job.py
    atlas/grid/jc_read.py

    scripts/grid_cp.sh
    python/filter_lines.py
    python/files_on_disk.py
    python/files_on_grid.py
    python/files_on_castor.py
    scripts/cp_from_castor.sh
    #scripts/split_file.sh
    scripts/replace_line.sh
    
    # TDAQ utilities
    python/tdaq_add_l1result.py 
    python/tdaq_add_l1result_split150.py 
    python/tdaq_add_l1result_split.py 
    python/tdaq_filter_rob.py 
    python/tdaq_check_headers.py 
    python/tdaq_check_rod.py 
    python/tdaq_dump_robmap.py 
    python/tdaq_addL1Result.py
    python/tdaq_add_roib.py
    python/tdaq_check_roi.py

    # Trigger configuration
    python/l1conf_cnv.py
    python/tm_display.py
    scripts/check_l1config.sh
    scripts/trigconf_l1items.sh
    scripts/ath_trigdb_help.sh

    # Utilities
    python/checkmail.py
)

python_modules=(\
    python/castor_util.py 
    python/athtools/atktools.py 
    python/athtools/cmtpack.py 
    python/tdaq/tdaq_tools.py
    python/tklog.py
    python/athtools/tm_xml2list.py
    python/split_file.py
    python/pbook_tools.py

    python/ajm.py 
    python/jobmgr.py
    python/taskmgr.py
    python/pathenatask.py

    # GANGA scripts
    scripts/ganga_status.py
    scripts/ganga_get.py

    # Grid tools
    atlas/grid/aat.py
    atlas/grid/agt.py
    atlas/grid/alt.py
)

python_module_executables=(
    python/athtools/tm_xml2list.py
    python/split_file.py
    python/jobmgr.py
    python/ajm.py 
)

curdir=`pwd`
cd $TKDEV_ROOT
mkdir -p ${TK_SWDIR}/bin
mkdir -p ${TK_SWDIR}/lib
mkdir -p ${TK_SWDIR}/include
mkdir -p ${TK_SWDIR}/python
mkdir -p ${TK_SWDIR}/share
# Install shell/python scripts
for a in $scripts; do
    dest=$TK_SWDIR/bin/`basename $a`
    installFile $a $dest "-f" "--preserve=mode,ownership,timestamps"
#    dest=$HOME/bin/`basename $a`
#    installFile $a $dest "-f" "--preserve=mode,ownership,timestamps"
done

# Install python modules
for a in $python_modules; do
    dest=$TK_SWDIR/python/`basename $a`
    installFile $a $dest "--preserve=mode,ownership,timestamps"
done

# Install python modules which are also executables
for a in $python_modules; do
    dest=$TK_SWDIR/bin/`basename $a`
    src=$TK_ROOT/python/`basename $a`
    if [[ ! -L $dest ]]; then 
	ln -s $src $dest
    fi
done

cd $curdir

