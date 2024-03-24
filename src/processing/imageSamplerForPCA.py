from os import listdir
from os.path import isfile, join
import imageio.v2 as imageio
from imageio import imread
import numpy as np
import json
 
path_images = r"02_output/images_resized/"
files = [f for f in listdir(path_images) if isfile(join(path_images, f))]

samples = {"gs":{}}
files = files[0:100]
for f in files:
	print(f)
	fileName = str(path_images)+"%s" % (f)
	split_fileName = f.split(".")
	image_name = split_fileName[0]
	image_ext = split_fileName[-1].lower()
	if image_ext in ["jpg","jpeg"]:
		src_image = imageio.imread("%s%s" % (path_images,f))
		src_image_shape = src_image.shape
		store_gs = []
		#gsArray = np.zeros((src_image_shape[0],src_image_shape[1]),dtype=int)
		for i in range(0,src_image_shape[0],1):
			for j in range(0,src_image_shape[1],1):
				pxl = src_image[i, j, :]
				gs = round((((pxl[0]*0.299)+(pxl[2]*0.587)+(pxl[1]*0.114))),2)
				store_gs.append(gs)
		samples["gs"][image_name] = store_gs
			
with open(str(
	"%s%s" % (r"02_output/images_resized/image_data/","samples.json")
	), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(samples, ensure_ascii=False))

print("DONE")
