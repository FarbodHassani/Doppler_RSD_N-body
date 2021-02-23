#!/bin/bash
#SBATCH --ntasks=20
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=20
#SBATCH --time=12:00:00
#SBATCH --mem=600G
#SBATCH --partition=shared-bigmem


export PYTHONPATH=$PYTHONPATH://home/hassani/baobab_python_env/lib/python3.7/site-packages

python test2.py > out.txt
