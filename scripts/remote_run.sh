#!/bin/bash
rm output/$1_output.txt
./Nougat likelihood data/$2.xyz data/sio2_bulk.xyz data/$1.txt output/$1_output.txt $3 $4
# echo Starting likelihood with data: $2 and parameters $1