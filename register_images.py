import SimpleITK as sitk
import os


INPUT_FOLDER = "D:\Geert\SOFT_TISSUE_THICK"
OUTPUT_FOLDER = "D:\Geert\SOFT_TISSUE_THICK_REGISTERED"


if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

elastix = sitk.SimpleElastix()
# elastix.LogToConsoleOn()

elastix.SetParameterMap(sitk.ReadParameterFile("translation.txt"))
elastix.AddParameterMap(sitk.ReadParameterFile("rigid_geert.txt"))
# # elastix.SetParameterMap(sitk.ReadParameterFile("affine_geert.txt"))
# elastix.SetParameterMap(sitk.ReadParameterFile("non_rigid.txt"))

atlas = sitk.ReadImage('atlas.mha')
elastix.SetFixedImage(atlas)

already_registered_scans = os.listdir(OUTPUT_FOLDER)

for scan_name in os.listdir(INPUT_FOLDER):
    if not scan_name in already_registered_scans:
        print("Working on {}".format(scan_name))
        relative_path = os.path.join(INPUT_FOLDER, scan_name)
        image = sitk.ReadImage(relative_path)
        image = sitk.Cast(image, sitk.sitkInt16)
        elastix.SetMovingImage(image)
        try:
            elastix.Execute()
        except RuntimeError as err:
            print("There was an error in {}.".format(scan_name))
        else:
            result_rigid = elastix.GetResultImage()
            sitk.WriteImage(result_rigid, os.path.join(OUTPUT_FOLDER, scan_name))
