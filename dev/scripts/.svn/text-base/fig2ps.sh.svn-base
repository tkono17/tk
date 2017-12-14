#!/usr/local/bin/zsh

function create_dvi() {
    if [[ ${#*} == 1 ]]; then
	print 'Need to provide a tex file to create_dvi';
	return -1;
    fi
    fname_tex=$1;
    latex $fname_tex;
    latex $fname_tex;
    latex $fname_tex;
    return $?;
}

function create_ps() {
    if [[ ${#*} == 1 ]]; then
	print 'Need to provide a dvi file to create_ps';
	return -1;
    fi
    fname_dvi=$1;
    dvips fname_dvi
    return $?;
}



fname_tex='fig.tex'

