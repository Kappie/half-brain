import os
import shutil
import SimpleITK as sitk


INPUT_FOLDER = "D:\Geert\Registry_H31S"
OUTPUT_FOLDER = "D:\Geert\Registry_bad_scans"
MINIMUM_SIZE = 200
MAXIMUM_SIZE = 460
DRY_RUN = False

for path in os.listdir(INPUT_FOLDER):
    image_path = os.path.join(INPUT_FOLDER, path)
    image = sitk.ReadImage(image_path)
    print("[reading] {}".format(image_path))
    n_slices = image.GetSize()[-1]
    if n_slices < MINIMUM_SIZE:
        print("[Too small] Moving {}. Only {} slices.".format(path, n_slices))
        if not DRY_RUN:
            shutil.move(image_path, os.path.join(OUTPUT_FOLDER, path))
    if n_slices > MAXIMUM_SIZE:
        print("[Too large] Warning: {} has {} slices".format(path, n_slices))
