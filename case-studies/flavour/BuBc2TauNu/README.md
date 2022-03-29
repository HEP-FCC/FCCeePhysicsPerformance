## Combined search for Bu and Bc to tau + nu decays

### Overview

This analysis is a spin-off of the Bc2TauNu search.
It inherits the basic steps from Bc2TauNu but aims to consider both Bc2TauNu and Bu2TauNu as separate signals.
This analysis will also be used as a benchmark to help optimize the generic [FCC analysis workflow](https://github.com/HEP-FCC/FCCAnalyses).


### Scripts

The following scripts are used to run the variois steps of the offline analysis:
- `user_config.py`: paths and common variables.
- `decay_mode_xs.py`: definitions of the branching ratios and cross-sections for the exclusive B-hadron modes considered as background.
- `train_xgb.py`: train first stage binary BDT.
- `train_xgb_stage2.py`: train second stage multi-class BDT.

### Development log

29.03.2022 Initial setup of this analysis. With only scripts for BDT training.
