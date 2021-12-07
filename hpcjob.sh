#!/bin/bash
#
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=48:00:00
#SBATCH --mem=4GB
#SBATCH --job-name=Local-Search
#SBATCH --mail-type=END
#SBATCH --mail-user=rtw262@nyu.edu
#SBATCH --output=slurm_%j.out

python3 localvsgreedy.py

