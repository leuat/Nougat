#!/bin/bash
echo parameters:
echo   1: owl 1-6  
echo   2: parameter file
rsync models/sio2_bulk.xyz models/$2.txt models/mcmc_model.xyz nicolaag@owl2:Fys2016/build/data/
rsync remote_run.sh nicolaag@owl2:Fys2016/build/
ssh nicolaag@owl$1 "cd Fys2016/build/;screen -d -m ./remote_run.sh mcmc_reproduce_pts $3"