#
# author: Lia Lavezzi - University of Torino & INFN - lia.lavezzi@to.infn.it
#

#!/bin/bash

#################### SETTINGS
pdg='e'
l_theta=(10 30 50 70 89)
l_ptot=(0.5 1 2 5 10 20 50 100)
####################

mkdir -p $SIM_OUTPUT_DIR/log  $SIM_OUTPUT_DIR/conv/hit  $SIM_OUTPUT_DIR/conv/track $SIM_OUTPUT_DIR/conv/mctrack $SIM_OUTPUT_DIR/sim  $SIM_OUTPUT_DIR/reco

# simulation
counter=0
total= $(( ${#l_theta[@]}*${#l_ptot[@]} ))
for theta in ${l_theta[@]}
do
    for ptot in ${l_ptot[@]}
    do
	echo "$counter / $total : electron momentum $ptot theta $theta"
	# simulation
	echo "SIMULATING"
	cd $SIM_INSTAL_DIR
	./bin/g4GMC ./g4mac/mymac/run_${pdg}_${theta}_${ptot}.mac geom_IDEA.txt 1 $SIM_OUTPUT_DIR >& $SIM_OUTPUT_DIR/log/log.txt
	# conversion
	echo "CONVERTING G4 -> ROME"
	cd $PRJBASE/converter
	./readHits $SIM_OUTPUT_DIR/hits00001.root 
	# reconstructing
	echo "RECONTRUCTING"
	cd $PRJBASE/analyzer/GMC
	mv $PRJBASE/converter/MCData00001.root  $PRJBASE/analyzer/GMC/.
	${PRJBASE}/analyzer/GMC/gmcanalyzer.exe -b -q -i geant4MC-IDEA.xml -r 1 >& out-hits_1.log
	${PRJBASE}/analyzer/GMC/gmcanalyzer.exe -b -q -i geant4MC-IDEA-fit.xml -r 1 >& out-reco_1.log
	# converting to EDM
        echo "CONVERTING ROME -> EDM"
	cd $PRJBASE/converter
	mv $PRJBASE/analyzer/GMC/RecoData00001.root   $SIM_OUTPUT_DIR/.
	./convertTracks $SIM_OUTPUT_DIR/RecoData00001.root
	# convertion of MC tracks
	echo "CONVERTING MC -> EDM"
	cd $PRJBASE/converter
	./convertHits $SIM_OUTPUT_DIR/hits00001.root

	# ----------------------------------------------------
	mv $SIM_OUTPUT_DIR/log/log.txt            $SIM_OUTPUT_DIR/log/out-sim_${pdg}_${theta}_${ptot}.log
	mv $SIM_OUTPUT_DIR/hits00001.root         $SIM_OUTPUT_DIR/sim/hits_${pdg}_${theta}_${ptot}.root
	mv $PRJBASE/analyzer/GMC/MCData00001.root $SIM_OUTPUT_DIR/conv/hit/MCDatas_${pdg}_${theta}_${ptot}.root
	mv $PRJBASE/analyzer/GMC/histos00001.root $SIM_OUTPUT_DIR/reco/histos_${pdg}_${theta}_${ptot}.root
	mv $PRJBASE/analyzer/GMC/MCHits00001.root $SIM_OUTPUT_DIR/reco/MCHits_${pdg}_${theta}_${ptot}.root
	mv $PRJBASE/analyzer/GMC/out-hits_1.log   $SIM_OUTPUT_DIR/log/out-hits_${pdg}_${theta}_${ptot}.log
	mv $PRJBASE/analyzer/GMC/out-reco_1.log   $SIM_OUTPUT_DIR/log/out-reco_${pdg}_${theta}_${ptot}.log
	mv $SIM_OUTPUT_DIR/RecoData00001.root     $SIM_OUTPUT_DIR/reco/RecoData_${pdg}_${theta}_${ptot}.root
	mv $PRJBASE/converter/test.root           $SIM_OUTPUT_DIR/conv/track/test_${pdg}_${theta}_${ptot}.root
	mv $PRJBASE/converter/EDMTracks00001.root $SIM_OUTPUT_DIR/conv/track/EDMTracks_${pdg}_${theta}_${ptot}.root
	mv $PRJBASE/converter/MCData00001.root    $SIM_OUTPUT_DIR/conv/mctrack/MCData00001_${pdg}_${theta}_${ptot}.root

	# if you need to save space
	rm $SIM_OUTPUT_DIR/log/out-sim_${pdg}_${theta}_${ptot}.log
	rm $SIM_OUTPUT_DIR/sim/hits_${pdg}_${theta}_${ptot}.root
        rm $SIM_OUTPUT_DIR/conv/hit/MCDatas_${pdg}_${theta}_${ptot}.root
        rm $SIM_OUTPUT_DIR/reco/histos_${pdg}_${theta}_${ptot}.root
        rm $SIM_OUTPUT_DIR/reco/MCHits_${pdg}_${theta}_${ptot}.root
        rm $SIM_OUTPUT_DIR/log/out-hits_${pdg}_${theta}_${ptot}.log
        rm $SIM_OUTPUT_DIR/log/out-reco_${pdg}_${theta}_${ptot}.log
        rm $SIM_OUTPUT_DIR/reco/RecoData_${pdg}_${theta}_${ptot}.root
        rm $SIM_OUTPUT_DIR/conv/track/test_${pdg}_${theta}_${ptot}.root
       
	counter=$(echo "$counter + 1" | bc)
    done
done

