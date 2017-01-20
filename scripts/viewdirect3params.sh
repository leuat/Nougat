#!/bin/bash
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 1d threshold $2
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 1d persistence $2
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 1d scale $2
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 2d threshold persistence $2
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 2d threshold scale $2
python plot_mc.py -save_plot -no_display results_$1/$1_output.txt 2d persistence scale $2
montage mcmc_1d_threshold.png mcmc_1d_persistence.png mcmc_1d_scale.png mcmc_2d_threshold_persistence.png mcmc_2d_threshold_scale.png mcmc_2d_persistence_scale.png  -tile 3x2 -geometry +0+0 results.png
open results.png
