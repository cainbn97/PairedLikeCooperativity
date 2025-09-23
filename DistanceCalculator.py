import pymol
import numpy as np


for object in cmd.get_object_list():
	matrix = np.zeros((60, 60))
	print("Starting " + str(object))
	for i in np.arange(1,61,1):
		for j in np.arange(1,61,1):
			try:
				distance_value = cmd.get_distance(f"/{object}/A/A/{i}/CA", f"/{object}/A/A/{j}/CA")
				matrix[i-1,j-1] = distance_value
			except:
				print(i); print(j)
				print("One residue in pair is missing.")

	matrix.tofile(str(object) + "_MainChainDistanceMatrix.txt", sep = "\t")

print('DONE!')
