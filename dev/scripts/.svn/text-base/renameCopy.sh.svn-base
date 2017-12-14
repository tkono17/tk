#!/usr/bin/env zsh

src_dir="${HOME}/gangadir/workspace/Local/53"
dest_dir="/space2/tkohno/data/ROOT/Zmumu"
in_file="muontest.root"
pattern="s/\.root/_\.root/"
subdirs=()

((i = 0))
while [[ $i -lt 40 ]]; do
    subdirs=($subdirs $i)
    ((i = $i + 1))
done

cd $src_dir;
for dir in $subdirs; do
    cd $dir/output;
    ls $in_file
    out_file=`echo $in_file | sed -e "s/\.root/_${dir}\.root/"`
    echo "in_file = `pwd`/$in_file"
    echo "out_file = $out_file"
    cp $in_file $dest_dir/$out_file
    cd -
done

