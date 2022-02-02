#!/bin/bash

for i in 5 10 12 15 20 30 40 50 70 90
do
    python3 analysis_HNL_read.py -i HNL_sample_creation/HNL_eenu_"$i"GeV_1p41e-6Ve.root
done
