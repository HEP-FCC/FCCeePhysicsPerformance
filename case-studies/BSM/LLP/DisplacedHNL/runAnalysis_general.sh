#!/bin/bash

python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zee_ecm91/events_199283914.root -o ./read_EDM4HEP/Zee/
python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zbb_ecm91/events_199984817.root -o ./read_EDM4HEP/Zbb/
python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Ztautau_ecm91/events_198604879.root -o ./read_EDM4HEP/Ztautau/
python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zuds_ecm91/events_199878624.root -o ./read_EDM4HEP/Zuds/
python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zcc_ecm91/events_199973752.root -o ./read_EDM4HEP/Zcc/
