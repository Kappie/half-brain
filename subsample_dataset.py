import os
import numpy as np
import itertools
import subprocess


def resample_all_images_in_folder(input_folder, output_folder, percentage):
    # c3d img1.img -resample 200% -o img2.img
    for image_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, image_name)
        output_path = os.path.join(output_folder, image_name)
        percentage_string = "{}%".format(percentage)
        subprocess.call(['c3d', input_path, '-resample', percentage_string, '-o', output_path])


DATA_FOLDER = "D:\Geert\SOFT_TISSUE_THICK_DATASET"
OUTPUT_BASE_FOLDER = "D:\Geert\SOFT_TISSUE_THICK_DATASET_DOWNSAMPLED"
AFFECTED_FOLDER = os.path.join(DATA_FOLDER, "AFFECTED")
UNAFFECTED_FOLDER = os.path.join(DATA_FOLDER, "UNAFFECTED")
INPUT_FOLDERS = [AFFECTED_FOLDER, UNAFFECTED_FOLDER]
OUTPUT_FOLDERS = [os.path.join(OUTPUT_BASE_FOLDER, folder) for folder in ["AFFECTED", "UNAFFECTED"]]
RESAMPLE_PERCENTAGE = 25

for folder in OUTPUT_FOLDERS:
    if not os.path.exists(folder):
        os.makedirs(folder)

for input_folder, output_folder in zip(INPUT_FOLDERS, OUTPUT_FOLDERS):
    resample_all_images_in_folder(input_folder, output_folder, RESAMPLE_PERCENTAGE)
