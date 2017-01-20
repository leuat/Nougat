#!/bin/bash
echo parameters:
echo   1: owl 1-6  
echo   2: dta or gofr - measure
echo   3: data file
echo   4: parameter file
echo   5: number of samples
echo   6: number of random vectors
rsync models/sio2_bulk.xyz models/$4.txt models/$3.xyz nicolaag@owl2:Fys2016/build/data/
rsync remote_run.sh nicolaag@owl2:Fys2016/build/
for run in {1..6}
do
	echo Starting likelihood with data: $4 and parameters $3 type $2
    ssh nicolaag@owl$1 "cd Fys2016/build/;screen -d -m ./remote_run.sh $2 $4 $3 $5 $6"
    sleep 0.5
done
