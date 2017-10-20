import os
import subprocess
import shutil
import SimpleITK as sitk
import numpy as np

# DATA_FOLDER = "D:\Registry\REGISTRY_NCCT_BL"
# OUTPUT_FOLDER = "NCCT_H31S"
# DATA_FOLDER = "Z:\Registry\REGISTRY_NCCT_BL"
DATA_FOLDER = "D:\Registry\Thick\REGISTRY_NCCT_BL"
OUTPUT_FOLDER = "D:\Geert\Registry_H31S_NEW"
OUTPUT_FORMAT = ".nii"
DELETE_FOLDERS = False


def select_h31s(scan_folders):
    """
    We assume the h31s scan is always the one with the most slices.
    """
    convolution_metadata_key = "0018|1210"
    for scan_folder in scan_folders:
        slice_paths = os.listdir(scan_folder)
        if slice_paths:
            first_slice_path = os.path.join( scan_folder, os.listdir(scan_folder)[0] )
            first_slice = sitk.ReadImage(first_slice_path)
            if first_slice.HasMetaDataKey(convolution_metadata_key):
                print(first_slice.GetMetaData(convolution_metadata_key))

    # number_of_slices = [len(os.listdir(folder)) for folder in scan_folders]
    # h31s_scan_index = np.argmax(number_of_slices)
    # return scan_folders[h31s_scan_index], number_of_slices[h31s_scan_index]
    return "todo"


if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

for subdir in os.listdir(DATA_FOLDER):
    # dirs with names R0001 etc.
    print("[{}] -------- ".format(subdir))
    relative_path_to_subdir = os.path.join(DATA_FOLDER, subdir)
    for subdir2 in os.listdir(relative_path_to_subdir):
        # dirs with names 26921455 etc.
        relative_path_to_subdir2 = os.path.join(DATA_FOLDER, subdir, subdir2)
        scan_folders = []
        # select all folders than contain a scan
        for scan_folder in os.listdir(relative_path_to_subdir2):
            # dirs with names 1.3.6.1.4.1.40744.9.163023911123769408425889577070193571061 etc.
            relative_path_to_scan_folder = os.path.join(relative_path_to_subdir2, scan_folder)
            if os.path.isdir(relative_path_to_scan_folder):
                scan_folders.append(relative_path_to_scan_folder)

        if scan_folders:
            select_h31s(scan_folders)
            # h31s_scan_folder, n_slices = select_h31s(scan_folders)
            # output_name = os.path.join(OUTPUT_FOLDER, subdir + OUTPUT_FORMAT)
            # # Usage: DicomSeriesReader <input_directory> <output_file>
            # command = "python DicomSeriesReader.py {} {}".format(h31s_scan_folder, output_name)
            # subprocess.call(command, shell=True)
            #
            # # delete all scan folders
            # if DELETE_FOLDERS:
            #     for folder in scan_folders:
            #         shutil.rmtree(folder)
