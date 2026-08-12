
# set the number of cores here
NP ?= 4

# run simulation
run-sim:
	cp -r 0.orig 0 
	setFields
	foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $(NP) -disableFunctionEntries
	decomposePar
	mpirun -np $(NP) renumberMesh -overwrite -parallel 
	mpirun -np $(NP) interFoam -parallel | tee interFoam.log  
	reconstructPar
	rm -r processor*

# generate straight-cylinder mangrove mesh
run-mesh:
	python system/getBlockMeshDict.py 
	blockMesh 
	topoSet
	foamDictionary system/refineMeshDict -entry set -set interface_region1
	refineMesh -overwrite
	topoSet
	foamDictionary system/refineMeshDict -entry set -set interface_region2
	refineMesh -overwrite
	topoSet
	-rm -r 0
	snappyHexMesh -overwrite
	checkMesh 

# generate mesh for empty flume 
run-empty:
	blockMesh -dict system/blockMeshDict_empty
	topoSet
	foamDictionary system/refineMeshDict -entry set -set interface_region1
	refineMesh -overwrite
	topoSet
	foamDictionary system/refineMeshDict -entry set -set interface_region2
	refineMesh -overwrite
	topoSet
	-rm -r 0
	checkMesh

# delete run-related files (except mesh)
clean-sim:
	foamListTimes -withZero -rm
	-rm -r ./postProcessing/
	-rm -r ./processor*
	-rm ./*.log
	-rm -r ./*.log.analyzed

# delete mesh-related files
clean-mesh:
	-find . -name "*Zone.Identifier" -type f -delete 
	-rm -r ./constant/polyMesh/
	-rm ./constant/triSurface/*.eMesh
	-rm -r ./constant/extendedFeatureEdgeMesh