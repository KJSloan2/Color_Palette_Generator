from datetime import datetime
from os import listdir
from os.path import isfile, join
import imageio.v2 as imageio
from imageio import imread
import numpy as np
import math
import json	
import csv

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

 
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import warnings
warnings.filterwarnings("ignore")
######################################################################################
######################################################################################
def plot_grayscale_histogram(grayscale_values):
	plt.hist(grayscale_values, bins=256, range=(0, 256), density=True, color='gray', alpha=0.7)
	plt.title('Grayscale Histogram')
	plt.xlabel('Pixel Intensity')
	plt.ylabel('Frequency')
	plt.show()

def computeHue(r,g,b):
	r_depth = r/255
	g_depth = g/255
	b_depth = b/255
	cMax = max(r_depth,g_depth,b_depth)
	cMin = min(r_depth,g_depth,b_depth)
	delta = (cMax - cMin)+1
	if cMax == r_depth:
		hue = (g_depth - b_depth) / (delta);
	elif cMax == g_depth:
		hue = 2 +(b_depth - r_depth) / (delta);
	elif cMax == b_depth:
		hue = 4 + (r_depth - g_depth) / (delta); 
	if hue > 0:
		hue = (round(hue*60,2))
	else:
		hue = (round(math.floor(360 + hue),2))
	return(hue)
######################################################################################
######################################################################################
step_size = 25
bounds = (0, 255-step_size)

# Create a meshgrid
x = np.arange(bounds[0], bounds[1] + step_size, step_size)
y = np.arange(bounds[0], bounds[1] + step_size, step_size)
z = np.arange(bounds[0], bounds[1] + step_size, step_size)

# Create a 3D grid using meshgrid
xx, yy, zz = np.meshgrid(x, y, z)

# Stack the points into a 3D array
ref = np.column_stack((xx.ravel(), yy.ravel(), zz.ravel()))
tableSize = ref.shape[0]
######################################################################################
def format_number(number):
    number_str = str(number)
    num_zeros = 3 - len(number_str)
    num_zeros = max(0, min(num_zeros, 2))
    formatted_number = '0' * num_zeros + number_str
    return formatted_number
######################################################################################
class HashTable:
	def __init__(self, size=tableSize):
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
#hash_table.display_table()

samples = {}
for i in range(len(ref)):
	key = "".join(map(str,list(map(format_number,ref[i]))))
	samples[key] = {
		"rgb":[int(ref[i][0]),int(ref[i][1]),int(ref[i][2])],
		"count":0, "images":{}}

refPointMaxDist =  math.sqrt((0 - 25)**2 + (0 - 25)**2 + (0 - 25)**2)
print(refPointMaxDist)
######################################################################################
path_textures = r"01_data/content/images/"
files = [f for f in listdir(path_textures) if isfile(join(path_textures, f))]
imPad = 2
sampleWindowSize = [3,3]
n = 0

ref_rgb = []

def round_to_5(value):
	return round(value / 5) * 5

pool_gs = []
pool_rbg = []
pool_hue = []
rgb_normalized = []
ref_rgbKeys = []
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
					dn = [mean_r, mean_b, mean_g]

					store_dist = []
					for refKey,refItem in samples.items():
						dist = math.sqrt(
							(float(refItem["rgb"][0])-float(dn[0]))**2 + 
							(float(refItem["rgb"][1])-float(dn[1]))**2 + 
							(float(refItem["rgb"][2])-float(dn[2]))**2)
						if dist < refPointMaxDist:
							refItem["count"] += 1
							if image_name not in list(refItem["images"].keys()):
								refItem["images"][image_name] = {
									"pts":[[int(x),int(y)]]
								}
							else:
								refItem["images"][image_name]["pts"].append([int(x),int(y)])
							break

						#dist.append(store_dist)
					#dist_argsort = np.argsort(dist)[::-1]
					#min_dist = dist[dist_argsort[-1]]

					'''if rgbKey not in ref_rgbKeys:
						ref_rgbKeys.append(rgbKey)
						gs = round((((mean_r*0.298)+(mean_g*0.587)+(mean_b*0.114))),2)
						hue = computeHue(mean_r,mean_g,mean_b)
						pool_gs.append(gs)
						pool_rbg.append(rgb)
						pool_hue.append(hue)
						rgb_normalized = [
							round((mean_r/255),2),
							round((mean_g/255),2),
							round((mean_b/255),2)
							]
						
						samples["rgb"][rgbKey] = {
							"count":1,
							"rgb":rgb,
							"gs":gs,
							"hue":hue,
							"normalized":rgb_normalized
						}
					else:
						samples["rgb"][rgbKey]["count"]+=1'''
					
######################################################################################			
'''sampled_rgb = []

samples_rgbCount = []
samples_rgbNormalized = []
for key,item in samples["rgb"].items():
	sampled_rgb.append(item["rgb"])
	samples_rgbCount.append(item["count"])
	samples_rgbNormalized.append(item["normalized"])
######################################################################################
def rgb_to_hex(r, g, b):
	hex_code = "#{:02x}{:02x}{:02x}".format(r, g, b)
	return hex_code

colorSpace = np.array(sampled_rgb)
def calculate_wcss(data, max_k):
	wcss = []
	for k in range(1, max_k + 1):
		kmeans = KMeans(n_clusters=k, random_state=42)
		kmeans.fit(data)
		wcss.append(kmeans.inertia_)
	return wcss'''

'''max_clusters = 25
#wcss_values = calculate_wcss(colorSpace, max_clusters)
 
distortions = []
inertias = []
mapping1 = {}
mapping2 = {}
K = range(1, 10)
X = colorSpace
for k in K:
	# Building and fitting the model
	kmeanModel = KMeans(n_clusters=k).fit(X)
	kmeanModel.fit(X)
 
	distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_,
										'euclidean'), axis=1)) / X.shape[0])
	inertias.append(kmeanModel.inertia_)
 
	mapping1[k] = sum(np.min(cdist(X, kmeanModel.cluster_centers_,
								   'euclidean'), axis=1)) / X.shape[0]
	mapping2[k] = kmeanModel.inertia_

def find_elbow(wcss_values):
	x = np.arange(1, len(wcss_values) + 1)
	y = np.array(wcss_values)

	second_derivative = np.diff(np.diff(y))
	elbow_index = np.argmax(second_derivative) + 2

	return elbow_index

elbow = find_elbow(inertias)

# Plot the elbow curve with the identified elbow point in 3D
fig = plt.figure(figsize=(8, 6))

plt.plot(range(1, max_clusters + 1), inertias, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.scatter(elbow, inertias[elbow - 1], c='red', label='Elbow Point', zorder=5)
plt.legend()

plt.savefig(r"%s%s" % ("02_output/plots/","optimalK.png"))

#rgb_values_normalized = (colorSpace - colorSpace.min(axis=0)) / (colorSpace.max(axis=0) - colorSpace.min(axis=0))


fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot with different colors for each class
scatter = ax.scatter(colorSpace[:, 0], colorSpace[:, 2], colorSpace[:, 1], c=samples_rgbNormalized, s=samples_rgbCount)

# Add labels and legend
ax.set_xlabel('R')
ax.set_ylabel('B')
ax.set_zlabel('G')
ax.set_title("Sampled Colors in 3d RBG Space")
colorbar = plt.colorbar(scatter, ticks=[0, 1, 2], orientation='vertical', label='Class')
plt.savefig(r"%s%s" % ("02_output/plots/","colorSamples3d.png"))'''


'''kmeans = KMeans(n_clusters=max_clusters)
kmeans.fit(colorSpace)
labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_

cluster_labels = kmeans.predict(kmeans.cluster_centers_)
output = {"colors":[]}
for label,clusterCenter in zip(cluster_labels,cluster_centers):
	print(label)
	cluster_rgb = [int(clusterCenter[0]),int(clusterCenter[2]),int(clusterCenter[1])]'''


#plot_grayscale_histogram(pool_gs)

with open(str(
	"%s%s" % (r"imageSpace/textures/","samples.json")
	), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(samples, indent=1, ensure_ascii=False))

print("DONE")
