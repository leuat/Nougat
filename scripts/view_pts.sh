#!/bin/bash
rm -rf results_pts
mkdir results_pts
scp nicolaag@capra.uio.no:~/Fys2016/build/output/mcmc_reproduce_pts_output.txt results_pts/
python plot_mc_all.py 2d 3 3 abc results_pts/mcmc_reproduce_pts_output.txt persistence threshold scale 
python plot_mc_all.py 1d 3 3 abc results_pts/mcmc_reproduce_pts_output.txt persistence threshold scale 
