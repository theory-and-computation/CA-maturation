mol new frame-ba.pdb type pdb
mol delrep 0 top
mol representation NewCartoon
mol color ColorID 10
mol material AOChalky
mol resolution 50
mol addrep top
mol representation VDW 1.4
mol selection "name CA and resid 97"
mol color Occupancy
mol material AOChalky
mol resolution 50
mol addrep top
mol representation VDW 1.4
mol selection "name CA and resid 97"
mol color Occupancy
mol material AOChalky
mol resolution 50
mol addrep top
mol representation VDW 1.4
mol selection "name CA and resid 17"
mol color Occupancy
mol material AOChalky
mol resolution 50
mol addrep top
mol representation VDW 1.4
mol selection "name CA and resid 167"
mol color Occupancy
mol material AOChalky
mol resolution 50
mol addrep top
mol representation VDW 1.4
mol selection "name CA and resid 100"
mol color Occupancy
mol material AOChalky
mol resolution 50
mol addrep top
mol representation VDW 1.4
mol selection "name CA and resid 157"
mol color Occupancy
mol material AOChalky
mol resolution 50
mol addrep top
mol representation VDW 1.4
mol selection "name CA and resid 7"
mol color Occupancy
mol material AOChalky
mol resolution 50
mol addrep top
mol representation VDW 1.4
mol selection "name CA and resid 150"
mol color Occupancy
mol material AOChalky
mol resolution 50
mol addrep top
mol representation VDW 1.4
mol selection "name CA and resid 122"
mol color Occupancy
mol material AOChalky
mol resolution 50
mol addrep top
mol representation VDW 1.4
mol selection "name CA and resid 122"
mol color Occupancy
mol material AOChalky
mol resolution 50
mol addrep top
display shadows on
display depthcue on
display cuemode linear
display ambientocclusion on
display background white
axes location off
material change ambient AOChalky 0.30
set filename "../images/render-11.tga"
render TachyonInternal $filename
puts "Rendering completed. Output saved as $filename."
quit
