#!/bin/bash
echo parameters:
echo   1: owl 1-6  
echo   2: data file
echo   3: parameter file
echo   4: number of samples
echo   5: number of random vectors
rsync models/sio2_bulk.xyz models/$3.txt models/$2.xyz nicolaag@owl2:Fys2016/build/data/
rsync remote_run.sh nicolaag@owl2:Fys2016/build/
for run in {1..6}
do
	echo Starting likelihood with data: $3 and parameters $2
    ssh nicolaag@owl$1 "cd Fys2016/build/;screen -d -m ./remote_run.sh $3 $2 $4 $5"
    sleep 0.5
done
