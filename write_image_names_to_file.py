import os

INPUT_FOLDER = "D:\Geert\SOFT_TISSUE_THICK_REGISTERED"
image_names_file = "soft_tissue_thick_registered.txt"
image_format = ".mha"


file_names = []
for file_name in os.listdir(INPUT_FOLDER):
    if file_name.endswith(image_format):
        file_names.append(file_name + "\n")

with open(os.path.join(INPUT_FOLDER, image_names_file), "w") as output:
    output.writelines(file_names)
