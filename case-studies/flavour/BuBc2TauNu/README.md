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

- `fit_MVA_dists.py`: In each category, fit event efficiencies of each of MVA1 and MVA2 (Bu or Bc) cut scans. Output splines.
- 'estimate_purity.py': Read splines and estimate signal and background yields. Scan MVA cuts for optimal signal purity, output to yields.json
- `make_selected_samples_for_templates.py`: Preselect events for fitting, write to pkl.
- `simultaneous_template_fit.py`: Generate pseudo-data and perform combined fit in two categories. If more than 1 pseudo-data, output to fit_results.json
 

### Development log

29.03.2022 Initial setup of this analysis. With only scripts for BDT training.
11.04.2022 Add steps for category decision and shape fitting
