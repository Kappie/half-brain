import os
import shutil

INPUT_FOLDER = r"D:\Geert\NCCT_THICK_DICOM"
OUTPUT_FOLDER = r"D:\Geert\SOFT_TISSUE_THICK"

scans = []
number = 0
for dirpath, subdirs, files in os.walk(INPUT_FOLDER):
    for file in files:
        if file.endswith(".mha"):
            number += 1
            full_path = os.path.join(dirpath, file)
            destination = os.path.join(OUTPUT_FOLDER, "scan_{}".format(number) + ".mha")
            print("full path: {} is now called scan_{}".format(full_path, number))
            # shutil.copyfile(full_path, destination)
