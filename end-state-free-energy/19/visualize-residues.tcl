mol new frame-ba.pdb type pdb waitfor all
mol delrep 0 top
mol selection "segname 0A0 and resid 1 to 145"
mol representation NewCartoon 0.5 40 3.5 0
mol color ColorID 12
mol material AOChalky
mol addrep top
mol selection "segname 0A0 and resid 146 to 231"
mol representation NewCartoon 0.5 40 3.5 0
mol color ColorID 14
mol material AOChalky
mol addrep top
color scale method BWR
mol representation Licorice
mol selection "resid 150 and not hydrogen"
mol color Name
mol material AOChalky
mol resolution 50
mol addrep top
mol representation Licorice
mol selection "resid 170 and not hydrogen"
mol color Name
mol material AOChalky
mol resolution 50
mol addrep top
mol representation Licorice
mol selection "resid 151 and not hydrogen"
mol color Name
mol material AOChalky
mol resolution 50
mol addrep top
mol representation Licorice
mol selection "resid 149 and not hydrogen"
mol color Name
mol material AOChalky
mol resolution 50
mol addrep top
mol representation Licorice
mol selection "resid 173 and not hydrogen"
mol color Name
mol material AOChalky
mol resolution 50
mol addrep top
display resize 1000 1000
display shadows off
display depthcue on
display cuemode linear
display ambientocclusion on
color Display Background white
axes location off
scale by 1.75
rotate x by 60
rotate z by 10
rotate y by 40
material change ambient AOChalky 0.25
set filename "../images/render-19.tga"
render TachyonInternal $filename
puts "Rendering completed. Output saved as $filename."
