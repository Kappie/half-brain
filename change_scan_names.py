import os
import shutil
import re


INPUT_FOLDER = r"D:\Geert\NCCT_THICK_DICOM"
FOLDERS_TO_CHANGE = ["D:\Geert\SOFT_TISSUE_THICK", "D:\Geert\SOFT_TISSUE_THICK_REGISTERED"]


def extract_registry_number_from_full_path(path):
    # R0001 etc.
    registry_number_pattern = r'(R\d{4})'
    match = re.search(registry_number_pattern, path)
    if match:
        return match.group(1)
    else:
        return None


number = 0
for dirpath, subdirs, files in os.walk(INPUT_FOLDER):
    for file in files:
        if file.endswith(".mha"):
            number += 1
            full_path = os.path.join(dirpath, file)
            registry_number = extract_registry_number_from_full_path(full_path)
            for folder in FOLDERS_TO_CHANGE:
                old_name = os.path.join(folder, "scan_{}.mha".format(number))
                new_name = os.path.join(folder, registry_number + ".mha")

                if os.path.isfile(old_name):
                    print("I'm going to change {} into {}".format(old_name, new_name))
                    os.rename(old_name, new_name)
                else:
                    print("{} does not exist.".format(old_name))
