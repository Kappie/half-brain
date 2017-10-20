import os
import subprocess
import shutil
import SimpleITK as sitk

DATA_FOLDER = "D:\Registry\Thick\REGISTRY_NCCT_BL"

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


for subdir in os.listdir(DATA_FOLDER):
    # R0001 etc.
    print("[{}] --------- ".format(subdir))
    abs_path = os.path.join(DATA_FOLDER, subdir)
    scan_folder = os.listdir(abs_path)[0]
    abs_path_scan_folder = os.path.join(abs_path, scan_folder)
    select_h31s([abs_path_scan_folder])
