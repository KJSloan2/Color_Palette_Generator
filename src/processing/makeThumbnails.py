import os
from os import listdir
from os.path import isfile, join
import json
import numpy as np
from datetime import datetime, timezone
from PIL import Image, ImageOps
######################################################################################
paths_ = json.load(open("%s%s" % ("00_resources/","paths.json")))

imageStatsRef_ = json.load(open("%s%s" % (r"02_output/","imageStats_ref.json")))
imageStatsRef_keys = list(imageStatsRef_.keys())
files_ = [f for f in listdir(paths_["content"]["images"]) if isfile(join(paths_["content"]["images"], f))]
for f in files_:
	parse_f  = f.split(".")
	if parse_f[-1].lower() == "jpg":
		impath =  "%s%s" % (paths_["content"]["images"],f)
		im = Image.open(impath)
		im_width, im_height = im.size
		max_dimension = 50
		if im_width > im_height:
			new_width = max_dimension
			new_height = int(im_height * (max_dimension / im_width))
		else:
			new_height = max_dimension
			new_width = int(im_width * (max_dimension / im_height))

		imResized = im.resize((new_width,new_height))
		imResized = imResized.convert("RGB")
		imResized.save(os.path.join(r"01_data/content/images/thumbnails/", f"{parse_f[0]}.jpg"))
print("DONE")