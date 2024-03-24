'''
This script shuttles images from a given location to the designated location in the data directory of the project.
Images are resized to smaller dimensions while maintaining their original aspect ratio.
This is done to lower computational load and time for other steps.
Images are each given a unique ID and meta data is written to a manifest.
The unique image ID and meta data manifest can be used to retrieve data about the original image if necessary. 
'''
import json
import os
from os import listdir
from os.path import isfile, join
import datetime
from datetime import datetime, timezone

from PIL import Image, ImageOps
######################################################################################
def format_number(number):
    number_str = str(number)
    num_zeros = 5 - len(number_str)
    num_zeros = min(num_zeros, 3)
    formatted_number = '0' * num_zeros + number_str
    return str(formatted_number)
######################################################################################
def get_directories_in_directory(directory_path):
    directory_list = [f.path for f in os.scandir(directory_path) if f.is_dir()]
    return directory_list
######################################################################################
#paths_ = json.load(open("%s%s" % (r"00_resources\\","paths.json")))
imageStats_ = {}
dirKey = "google"

'''directories = get_directories_in_directory(r"{}/{}/".format(r"",dirKey))
dirPath = r"{}/{}/".format(r"",dirKey)
files_ = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
print(files_)
######################################################################################
for dir in directories:
	parse_dir = dir.split("/")
	dirId = parse_dir[-1]
	print(dirId)'''

dirPath = r"{}/{}/".format(r"PATH TO DIRECTORY OF IMAGES",dirKey)
files_ = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
imId = 0
for f in files_:
	parse_f  = f.split(".")
	if parse_f[-1].lower() in ["jpg","jpeg"]:
		print(f)
		impath =  "%s%s%s" % (dirPath,"/",f)
		im_stats = os.stat(impath)
		im_created = im_stats.st_ctime
		im_modified = im_stats.st_mtime
		im_cretaed_formated = datetime.fromtimestamp(im_stats.st_ctime, tz=timezone.utc)
		im_modified_formated = datetime.fromtimestamp(im_stats.st_mtime, tz=timezone.utc)
		date_modified = im_modified_formated.strftime("%m/%d/%Y")
		im = Image.open(impath)
		im_width, im_height = im.size
		max_dimension = 150
		if im_width > im_height:
			new_width = max_dimension
			new_height = int(im_height * (max_dimension / im_width))
		else:
			new_height = max_dimension
			new_width = int(im_width * (max_dimension / im_height))
		try:
			imResized = im.resize((new_width,new_height))
			imResized = imResized.convert("RGB")
			parse_dateModified = date_modified.split("/")
			imName = "_".join([
				dirKey,
				dirKey,format_number(imId),
				str(parse_dateModified[2]),
				str(parse_dateModified[0]),
				str(parse_dateModified[1])])
			imResized.save(os.path.join(r"01_data/textures/", f"{imName}.jpg"))
			imageStats_[imName] = {
				"image_name_original":parse_f[0],
				"width_orig":im_width,"height_orig":im_height,
				"width_new":new_width,"height_new":new_height,				
				"date_modified":date_modified
			}
			imId+=1
		except Exception as e:
			print(f"Error processing {f}: {e}")
			pass
######################################################################################
with open(str(
	"%s%s" % (r"02_output/","imageStats_ref.json")
	), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(imageStats_, indent=4, ensure_ascii=False))
######################################################################################
######################################################################################
print("DONE")