import json
import csv
import math
import numpy as np

refColors_refIds = []
referenceColors = {}
#CATEGORY	NAME	HEXCODE	R	G	B
with open(r"00_resources/referenceColors.csv", mode='r',newline='') as data_csv:
	csv_reader = csv.reader(data_csv)
	next(csv_reader)
	for row in csv_reader:
		hexcode = row[2]
		refColors_refIds.append(hexcode)
		referenceColors[hexcode] = {
			"category":row[0],
			"name":row[1],
			"rgb":[float(row[3]),float(row[4]),float(row[5])]
		}

groups = ["None","Yellow","Orange","Pink","Red","Brown","Green","Cyan","Blue","Purple","White","Grey"]

pallet_json = json.load(open(r"02_output/pallet.json"))

pool_clusterSize = []
pantoneNames = []
for colorObj in pallet_json["colors"]:
	pool_clusterSize.append(colorObj["cluster_size"])
	pantoneNames.append(colorObj["pantone_name"])

set_pantoneNames = list(dict.fromkeys(pantoneNames))
print(len(pantoneNames),len(set_pantoneNames))

#sorted_clusterSize = sorted(pool_clusterSize)
#argsort_clusterSize = list(map(str, list(np.argsort(pool_clusterSize)[::-1])))
'''argsort_clusterSize = list(np.argsort(pool_clusterSize))
output = {"colors":[]}
with open("%s%s" % (r"src\\","colorStats.csv"), 'w',newline='', encoding='utf-8') as write_dataOut:
	writer_dataOut = csv.writer(write_dataOut)
	writer_dataOut.writerow([
		"hex","r","g","b","gs","cluster_size","pantone_hex","pantone_name","group_id","cluster_id",
		"ref_cat","ref_name"
		])
	for i in range(len(pallet_json["colors"])):
		colorObj = pallet_json["colors"][i]
		colorObj["cluster_size_rank"] = int(argsort_clusterSize.index(i))
		print(colorObj["cluster_size_rank"])
		dist = []
		for refColorHex,refColorObj in referenceColors.items():
			ccDelta = math.sqrt(
				(float(refColorObj["rgb"][0])-float(colorObj["rgb"][0]))**2 + 
				(float(refColorObj["rgb"][2])-float(colorObj["rgb"][2]))**2 + 
				(float(refColorObj["rgb"][1])-float(colorObj["rgb"][1]))**2)
			dist.append(ccDelta)
		dist_argsort = np.argsort(dist)[::-1]
		min_dist = dist[dist_argsort[-1]]
		if min_dist <= 30:
			refColor = referenceColors[refColors_refIds[dist_argsort[-1]]]
			colorObj["group"] = groups.index(refColor["category"])
			colorObj["ref_category"] = refColor["category"]
			colorObj["ref_name"] = refColor["name"]
		else:
			colorObj["group"] = 0
			colorObj["ref_category"] = "None"
			colorObj["ref_name"] = "None"

		#for childColor in colorObj["colors"]:
		if colorObj["pantone_hex"] != None:
			output["colors"].append(colorObj)	
			writer_dataOut.writerow([
				colorObj["hex"],colorObj["rgb"][0],colorObj["rgb"][1],colorObj["rgb"][2],
				colorObj["gs"],colorObj["cluster_size"],colorObj["pantone_hex"],colorObj["pantone_name"],
				colorObj["group"],colorObj["cluster_id"],colorObj["ref_category"],colorObj["ref_name"]
			])
write_dataOut.close()

with open(str(
	"%s%s" % (r"src\\","pallet.json")
	), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(output, indent=2, ensure_ascii=False))

print("DONE")'''
