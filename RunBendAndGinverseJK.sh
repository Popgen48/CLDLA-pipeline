#!/bin/bash

speciesabbreviation="ECA" #also check number of chromosomes
projectname="ERU04nf"

for i in {1..31}
do
    if [ $i -le 9 ]
    then
	cd /data/medugorac/Shared/cLDLAsnpDip/${projectname}/${speciesabbreviation}0${i}/sw40snp/
	chmod ugo+x cLDLA_snp5
	chmod ugo+x Bend5
	chmod ugo+x ginverse
	cat ${projectname}.Chr_${i}.LinuxNC   |tr -d '\015' > ${projectname}.Chr_${i}.Linux
	sh RunAsrmelSeq.sh ${projectname}.Chr_${i}.Linux
    else
	cd /data/medugorac/Shared/cLDLAsnpDip/${projectname}/${speciesabbreviation}${i}/sw40snp/
	chmod ugo+x cLDLA_snp5
	chmod ugo+x Bend5
	chmod ugo+x ginverse
	cat ${projectname}.Chr_${i}.LinuxNC   |tr -d '\015' > ${projectname}.Chr_${i}.Linux
	sh RunAsrmelSeq.sh ${projectname}.Chr_${i}.Linux
    fi
done
