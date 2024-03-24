import json
from datetime import datetime
from os import listdir
from os.path import isfile, join

import numpy as np

import imageio.v2 as imageio
from imageio import imread
######################################################################################
######################################################################################
#maxGSVal = round((((255*0.298)+(255*0.587)+(255*0.114))),2)

class HashTable:
	def __init__(self, size=10):
		self.size = size
		self.table = [None] * size

	def _hash_function(self, key):
		return hash(key) % self.size

	def insert(self, key, value):
		index = self._hash_function(key)
		if self.table[index] is None:
			self.table[index] = []
		self.table[index].append((key, value))

	def get(self, key):
		index = self._hash_function(key)
		if self.table[index] is not None:
			vals = []
			for stored_key, value in self.table[index]:
				if stored_key == key:
					vals.append(value)
			return vals
		raise KeyError(f"Key '{key}' not found in the hash table.")

	def remove(self, key):
		index = self._hash_function(key)
		if self.table[index] is not None:
			for i, (stored_key, _) in enumerate(self.table[index]):
				if stored_key == key:
					del self.table[index][i]
					return
		raise KeyError(f"Key '{key}' not found in the hash table.")

	def display_table(self):
		for index, slot in enumerate(self.table):
			print(f"Index {index}: {slot}")
			
######################################################################################
hash_table = HashTable()
######################################################################################
path_textures = r"01_data/content/images/"
files = [f for f in listdir(path_textures) if isfile(join(path_textures, f))]
imPad = 2
sampleWindowSize = [3,3]
n = 0

samples = {"pixle_dn":[]}
ref_rgb = []

def round_to_5(value):
    return round(value / 5) * 5

for f in files:
	print(f)
	fileName = str(path_textures)+"%s" % (f)
	split_fileName = f.split(".")
	image_name = split_fileName[0]
	image_ext = split_fileName[-1].lower()
	if image_ext in ["jpg", "jpeg"]:
		src_image = imageio.imread("%s%s" % (path_textures,f))
		src_image_shape = src_image.shape

		(palX,palY) = (
			   int(src_image_shape[0]*.5/sampleWindowSize[0]),
				int(src_image_shape[1]*.5/sampleWindowSize[1])
				)
		  
		(poolX, poolY) = (sampleWindowSize[0],sampleWindowSize[1])
		nPixels = palX*palY

		iLen = palX+imPad
		jLen = palY+imPad

		for i in range(1,palX-1,1):
			x = int(i*poolX)
			for j in range(1,palY-1,1):
				y = int(j*poolY)
				pool = src_image[x:int(x+poolX), y:int(y+poolY), :]
				(pool_r,pool_g,pool_b) = ([],[],[])
				for subArray in pool:
					list(map(lambda rgb: pool_r.append(rgb[0]),subArray))
					list(map(lambda rgb: pool_g.append(rgb[1]),subArray))
					list(map(lambda rgb: pool_b.append(rgb[2]),subArray))
				if len(pool_r) >-0:
					mean_r = int(np.mean(pool_r))
					mean_g = int(np.mean(pool_g))
					mean_b = int(np.mean(pool_b))
					rgb = [mean_r, mean_g, mean_b]
					rgbKey = "_".join(map(str,[round_to_5(mean_r),round_to_5(mean_g),round_to_5(mean_b)]))
					hash_table.insert(rgbKey, fileName)
					'''if rgbKey not in ref_rgb:
						ref_rgb.append(rgbKey)
						samples["pixle_dn"][rgbKey]= {
							"rgb":rgb,
							"pixel_coords":[x,y],
							"images":[image_name]
							}'''
hash_table.display_table()
with open(str(
	"%s%s" % (r"02_output//","samples.json")
	), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(samples, ensure_ascii=False))

print("DONE")
