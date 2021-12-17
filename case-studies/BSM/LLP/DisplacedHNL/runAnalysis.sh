#!/bin/bash

for i in 30 50 90
do
    python3 analysis_HNL_read.py -i HNL_sample_creation/HNL_eenu_"$i"GeV_1p41e-6Ve.root
done
