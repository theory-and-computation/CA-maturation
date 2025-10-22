#!/bin/bash

export AMBERHOME=/home/ethan/anaconda3/envs/AmberTools23

for pdb_file in frame-*.pdb; do
    if [[ "$pdb_file" == *"-fixed.pdb" || "$pdb_file" == *"-done.pdb" ]]; then
        continue
    fi

    frame_num=$(echo "$pdb_file" | grep -oP '(?<=frame-)\d+')

    pdb4amber -i "$pdb_file" -o fixed.pdb --nohyd
    python rename.py

    cat > tleap.in << EOF
source leaprc.protein.ff14SB
source leaprc.water.tip3p

com = loadpdb done.pdb
set default PBRadii mbondi2

saveamberparm com frame.prmtop frame.inpcrd
solvatebox com TIP3PBOX 16.0
charge com

addions com Na+ 4
addionsrand com Na+ 50
addionsrand com Cl- 50
charge com

saveamberparm com complex-solvated.prmtop complex-solvated.inpcrd

quit
EOF

    $AMBERHOME/bin/tleap -s -f tleap.in

    if [[ ! -s frame.inpcrd ]]; then
        echo "Error: frame.inpcrd not properly generated for $pdb_file"
        continue
    fi

    sync
    sleep 1

    rm -f frame-ntd.prmtop frame-ntd.inpcrd
    rm -f frame-ctd.prmtop frame-ctd.inpcrd

    parmed -p frame.prmtop -c frame.inpcrd << EOF
strip :151-221
outparm frame-ntd.prmtop frame-ntd.inpcrd
quit
EOF

    parmed -p frame.prmtop -c frame.inpcrd << EOF
strip :1-150
outparm frame-ctd.prmtop frame-ctd.inpcrd
quit
EOF

done

rm -f fixed_nonprot.pdb fixed_renum.txt fixed_sslink leap.log mdinfo

