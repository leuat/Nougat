#!/bin/bash
rm output/$1_output.txt
./Nougat likelihood data/mcmc_model.xyz data/sio2_bulk.xyz data/$1.txt output/$1_output.txt $2 
