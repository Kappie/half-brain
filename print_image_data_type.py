import os
import subprocess
import shutil
import SimpleITK as sitk

INPUT_FOLDER = "D:\Geert\SOFT_TISSUE_THICK"


for scan_path in os.listdir(INPUT_FOLDER):
    full_path = os.path.join(INPUT_FOLDER, scan_path)
    scan = sitk.ReadImage(full_path)
    print(scan.GetPixelIDTypeAsString())
