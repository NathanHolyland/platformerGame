import json
from PIL import Image
import os.path

image_path = input("Input Level Image Path: ")
image = Image.open(image_path)
image_resolution = list(image.size)
json_path = input("Input Json Path: ")
pix = image.load()

print(os.path.isfile(json_path))
if not os.path.isfile(json_path):
    template_dict = {"Start": [], "Finish": [], "Bricks": [], "Enemies": []}
    dot = json_path.find(".")
    print(dot)
    if dot == -1:
        json_path += ".json"
    else:
        if json_path[dot:len(json_path)] != "json":
            json_path.replace(json_path[dot:len(json_path)], "json")
    new_file = open(json_path, "x")
    json.dump(template_dict, new_file, ensure_ascii=False, indent=4)
    new_file.close()


with open(json_path, 'r', encoding='utf-8') as f:
    json_dict = json.load(f)
    for y in range(image_resolution[1]):
        for x in range(image_resolution[0]):
            print(pix[x, y])
            if pix[x, y] == (0, 0, 0):
                json_dict["Bricks"].append([x, y])
            if pix[x, y] == (255, 0, 0):
                json_dict["Enemies"].append([x, y])
            if pix[x, y] == (0, 255, 0):
                json_dict["Finish"].append([x, y])
            if pix[x, y] == (0, 0, 255):
                json_dict["Start"].append([x, y])

with open(json_path, 'w', encoding='utf-8') as f:
    json_str = json.dumps(json_dict)
    json.dump(json_dict, f, ensure_ascii=False, indent=4)




