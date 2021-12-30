#!/bin/bash -x

if [[ `basename $PWD` != "MCProd" ]]; then echo "Execute from MCProd dir"; exit; fi
if [[ $# < 1 ]]; 
then 
    echo "Usage: ./generateEvents.sh <mg script> [delphes card]"
    echo "Example: ./generateEvents.sh $PWD/test/test.mg $PWD/delphes/cards/gen_card.tcl"
    exit
else
    mgScript=$1
    if [[ $# -gt 1 ]]; then
	delphesCard=$2
    else
	delphesCard="cards/gen_card.tcl"
    fi
fi

#source setup.sh

touch .dummy

#########################################################################

python MG5_aMC_v3_3_1/bin/mg5_aMC < "${mgScript}"
if [[ $? -ne 0 ]]; then
    echo "MadGraph ERROR"
    exit
fi

gzs=`find . -newer .dummy -name "unweighted_events.lhe.gz" -exec echo $PWD/{} \;`
echo $gzs

#------------------------------------------------------------------------

for gz in $gzs; do
    lhe=${gz%%.gz}
    pythiaOutput=${lhe%%.lhe}.hepmc
    delphesOutput=${lhe%%.lhe}.root  #set delphes output path/name
    gunzip $gz

    cd `dirname $lhe`
    $prodBase/MG5_aMC_v3_3_1/HEPTools/bin/MG5aMC_PY8_interface $prodBase/Cards/pythia8_card_noPlaceholders.dat
    #$prodBase/MG5_aMC_v3_3_1/HEPTools/bin/MG5aMC_PY8_interface $prodBase/Cards/pythia8_card_kk.dat
    if [[ $? -ne 0 ]]; then
	echo "Pythia  ERROR"
	exit
    fi
done

#------------------------------------------------------------------------

#cd delphes
for gz in $gzs; do 
    #DelphesLHEF  $delphesCard $delphesOutput $lhe
    DelphesHepMC2 $delphesCard $delphesOutput $pythiaOutput
    if [[ $? -ne 0 ]]; then
        echo "Delphes ERROR"
	exit
    fi
done

#------------------------------------------------------------------------
#source $prodBase/rivetenv.sh
#source /cvmfs/sft.cern.ch/lcg/releases/LCG_99/ROOT/v6.22.06/x86_64-centos7-gcc10-opt/ROOT-env.sh
#------------------------------------------------------------------------

for gz in $gzs; do
    lhe=${gz%%.gz}
    pythiaOutput=${lhe%%.lhe}.hepmc

    #cd `dirname $hepmc`
    rivet --analysis=MC_GENERIC $pythiaOutput
    rivet-mkhtml Rivet.yoda
    if [[ $? -ne 0 ]]; then
        echo "Rivet ERROR"
	exit
    fi
done
