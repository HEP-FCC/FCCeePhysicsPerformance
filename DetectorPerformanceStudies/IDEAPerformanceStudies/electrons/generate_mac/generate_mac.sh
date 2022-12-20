#
# author: Lia Lavezzi - University of Torino & INFN - lia.lavezzi@to.infn.it
#

#!/bin/bash

########################## SETTINGS
nevt=10000
pdg='e'
macdir=$SIM_INSTAL_DIR/g4mac/mymac
##########################

mkdir -p $macdir

for theta in 10 30 50 70 89 #110 130 150 170 190
do
    for ptot in 0.5 1 2 5 10 20 50 100
    do
	echo $pdg $ptot $theta
	echo "/random/setSeeds $RANDOM$RANDOM $RANDOM$RANDOM" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/run/initialize" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/gps/verbose 0" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/gps/particle $pdg-" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/gps/number 1" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/gps/pos/centre 0 0 0 cm" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/gps/ang/type iso" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/gps/ang/mintheta $theta deg" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/gps/ang/maxtheta $theta deg" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/gps/ang/minphi 0 deg" >> run_${pdg}_${theta}_${ptot}.mac
	echo "/gps/ang/maxphi 360 deg" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/gps/ene/mono $ptot GeV" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/field/update" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/field/setFieldZ 2.0 tesla" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/vis/modeling/trajectories/create/generic" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/tracking/verbose 0" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/hits/verbose 0" >> run_${pdg}_${theta}_${ptot}.mac 
	echo "/run/beamOn $nevt" >> run_${pdg}_${theta}_${ptot}.mac
    done
done

mv run*.mac ${macdir}/.
