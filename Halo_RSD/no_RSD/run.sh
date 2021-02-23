#!/bin/bash
#SBATCH --ntasks=20
#SBATCH --cpus-per-task=1
#SBATCH --ntasks-per-node=20
#SBATCH --time=12:00:00
#SBATCH --mem=600G
#SBATCH --partition=shared-bigmem


#. ~/baobab_python_env/bin/activate

module load GCCcore/8.3.0
module load Python/3.7.4 


export PYTHONPATH=$PYTHONPATH:/home/hassani/baobab_python_env/lib/python3.7/site-packages

export PYTHONPATH=$PYTHONPATH:/home/hassani/Pylians3/library/build/lib.linux-x86_64-3.7

python ref.py > out.txt
