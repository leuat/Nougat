#!/bin/bash
rm output/$2_output.txt
./Nougat likelihood $1 data/$3.xyz data/sio2_bulk.xyz data/$2.txt output/$2_output.txt $4 $5 $6
# echo Starting likelihood with data: $2 and parameters $1