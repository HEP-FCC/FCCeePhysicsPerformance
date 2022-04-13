#!/bin/bash

for i in 0p5 0p9 1p0 1p5 1p9
do
    python3 analysis_ALP.py -i ALP_sample_creation/ALP_Z_aa_1GeV_cYY_"$i".root
done