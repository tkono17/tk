#!/usr/bin/env zsh

castor_in_dir=''
castor_out_dir=''
input_files=()
output_files=()
#TAG-INSRET-castor_in_dir
#TAG-INSRET-castor_out_dir
#TAG-INSERT-input_files
#TAG-INSERT-output_files

stdout='lxbatch.out'
stderr='lxbatch.err'
#TAG-INSERT_stdout
#TAG-INSERT_stderr

command='echo'
args=''
#TAG-INSERT_command
#TAG-INSERT_args

#------------------------------------------------------------------------
#------------------------------------------------------------------------

# Copy input files to local area
echo "Copying input files to local area"
for file in $input_files; do
    cp_from_castor.sh -d . -l $castor_in_dir -f $file
done

echo "Running ..."
command=echo
args=""
$command $arg >$stdout 2>$stderr

# Copy output files to CASTOR
echo "Copying output files to CASTOR"
for file in $output_files; do
    cp_to_castor.sh -d . -l $castor_out_dir -f $file
done

echo "Done"
