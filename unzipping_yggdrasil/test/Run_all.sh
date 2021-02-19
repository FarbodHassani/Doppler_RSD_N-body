#!/bin/sh


ll=0;

for ((i = 0 ; i < 5 ; i++)); do
	for ((j = 0 ; j < 96 ; j++)); do

	ll=$((ll+1));
	ii=$i
	jj=$j
	echo $ll
	sed -e 's/gzip -d .\/..\/output\/w0d9_cs1_gevolution_snap000_cdm.0.gz/gzip -d .\/..\/output\/w0d9_cs1_gevolution_snap00'$i'_cdm.'$j'.gz/g' compress.batch > uncompress_$ll.batch
	chmod 750 uncompress_snap_$ll.batch
	sbatch uncompress_snap_$i_num_$j.batch
    done
    done
