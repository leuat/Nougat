#!/bin/bash
rm -rf results_$1
mkdir results_$1
rsync nicolaag@owl2:~/Fys2016/build/output/$1_output.txt results_$1/
#python plot_mc_all.py 2d 2 2 abc results_$1/$1_output.txt $2 $3 
#python plot_mc_all.py 1d abc 2 2 results_$1/$1_output.txt $2 $3 
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 1d threshold $2
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 1d persistence $2
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 2d threshold persistence $2
montage mcmc_1d_threshold.png mcmc_1d_persistence.png mcmc_2d_threshold_persistence.png  -tile 3x1 -geometry +0+0 results.png
open results.png
