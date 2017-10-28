import pandas
import SimpleITK as sitk
import os
import numpy as np

affected_hemispheres_file = r"D:\Geert\Registry_affected_sides.xls"
INPUT_FOLDER = r"D:\Geert\SOFT_TISSUE_THICK_SKULL_STRIPPED"
AFFECTED = r"D:\Geert\SOFT_TISSUE_THICK_DATASET\AFFECTED"
UNAFFECTED = r"D:\Geert\SOFT_TISSUE_THICK_DATASET\UNAFFECTED"


data = pandas.read_excel(affected_hemispheres_file).values
n_patients = data.shape[0]
LEFT_HEMISPHERE = "Left hemisphere"
RIGHT_HEMISPHERE = "Right hemisphere"


def separate_hemispheres(image):
    X, Y, Z = image.GetSize()
    # GetArrayFromImage flips x and z axes? Anyway, x-axis is the third axis.
    image_array = sitk.GetArrayFromImage(image)
    left_hemisphere = sitk.GetImageFromArray( image_array[:, :, :X//2] )
    right_hemisphere_array = image_array[:, :, X//2:]
    # We mirror the right hemisphere, so that it has the same orientation as the right hemisphere.
    right_hemisphere = sitk.GetImageFromArray( right_hemisphere_array[:, :, ::-1] )
    return left_hemisphere, right_hemisphere


# Make lookup table from excel sheet.
affected_hemispheres = {}
for i in range(n_patients):
    patient_nr = data[i, 0]
    affected_side = data[i, 1]
    affected_hemispheres[patient_nr] = affected_side


for scan_name in os.listdir(INPUT_FOLDER):
    image = sitk.ReadImage(os.path.join(INPUT_FOLDER, scan_name))
    left_hemisphere, right_hemisphere = separate_hemispheres(image)
    patient_nr = scan_name.split(".")[0]
    affected_path = os.path.join(AFFECTED, scan_name)
    unaffected_path = os.path.join(UNAFFECTED, scan_name)

    if affected_hemispheres[patient_nr] == LEFT_HEMISPHERE:
        sitk.WriteImage(left_hemisphere, affected_path)
        sitk.WriteImage(right_hemisphere, unaffected_path)
    elif affected_hemispheres[patient_nr] == RIGHT_HEMISPHERE:
        sitk.WriteImage(right_hemisphere, affected_path)
        sitk.WriteImage(left_hemisphere, unaffected_path)
    else:
        print("Neither hemisphere affected for {}. Not including in data set.".format(scan_name))
