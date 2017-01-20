#!/bin/bash
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 1d threshold $2
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 1d persistence $2
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 2d threshold persistence $2
montage mcmc_1d_threshold.png mcmc_1d_persistence.png mcmc_2d_threshold_persistence.png  -tile 3x1 -geometry +0+0 results.png
open results.png
