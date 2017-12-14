#!/usr/local/bin/zsh

function create_tex() {
    echo "print tex"
    if [[ ${#*} -eq 2 ]]; then
	echo 'Need to provide the output filename (tex) and list of figures to create_tex'
	return -1;
    fi
    
}

function create_tex_until_begin_document() {
echo "\\documentclass[landscape]{seminar}"
echo ""
echo "\\\usepackage{color}"
echo "\\\usepackage{graphicx}"
echo ""
echo "\\\slideframe{none}"
echo "\\\renewcommand{\slidetopmargin}{0mm}"
echo "\\\renewcommand{\slidebottommargin}{0mm}"
echo "\\\renewcommand{\slideleftmargin}{0mm}"
echo "\\\renewcommand{\sliderightmargin}{0mm}"
echo ""
echo "\\\pagestyle{plain}"
echo ""
echo "\\\begin{document}"
}

function create_tex_from_end_document() {
echo "\\\end{document}"
}

figs=()
if [[ ${#*} -lt 1 ]]; then
    echo 'Need to provide a list of figures to fig2tex'
    return -1;
else
    for f in $@; do
	figs=($figs $f)
    done
fi


# for f in $figs; do
#     echo "fig: $f";
# done


create_tex_until_begin_document
for f in $figs; do
    echo "  \\\begin{slide}"
    echo "    \\\begin{center}"
    echo "      \\\includegraphics[]{$f}"
    echo "    \\\end{center}"
    echo "  \\\end{slide}"
done;
create_tex_from_end_document

