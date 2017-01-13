#!/bin/bash
rm -rf results_$1
mkdir results_$1
rsync nicolaag@owl2:~/Fys2016/build/output/mcmc_reproduce_$1_output.txt results_$1/
#python plot_mc_all.py 2d 2 2 abc results_$1/mcmc_reproduce_$1_output.txt persistence threshold 
python plot_mc_all.py 1d abc 2 2 results_$1/mcmc_reproduce_$1_output.txt $2 $3 
