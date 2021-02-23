#!/bin/sh

files=("gevolution_boxsize_4032_ngrid_4608_lcdm_05062020" "gevolution_boxsize_4032_ngrid_4608_w_0m9_cs2_1_05062020" "gevolution_boxsize_4032_ngrid_4608_w_0m9_cs2_em7_05062020" "kevolution_boxsize_4032_ngrid_4608_w_0m9_cs2_em4_05062020" "kevolution_boxsize_4032_ngrid_4608_w_0m9_cs2_em7_05062020")
redshifts=("3" "2" "1" "0.5" "0")

data1=("0" "1" "2" "3" "4")
redshift1=("0" "1" "2" "3" "4")


ll=0;
for ((j = 0 ; j < 5 ; j++)); do
    data=${data1[$j]}

    for ((i = 0 ; i < 5 ; i++)); do
	redshift=${redshift1[$i]}

	ll=$((ll+1));

	output_dir=${files[$j]}_z_${redshifts[$i]}
	echo $output_dir;

	sed -e 's/j=0/j='$data'/g' -e 's/i=0/i='$redshift'/g' ref.py> ./Code_$output_dir.py

	sed -e 's/python ref.py > out.txt/python Code_'$output_dir.py' > out_Code_'$output_dir.txt'/g' run.sh > Run_$output_dir.sh
	#
	sbatch Run_$output_dir.sh
    done
    done
