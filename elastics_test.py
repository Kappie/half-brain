import SimpleITK as sitk

# sitk.Elastix.LogToConsoleOn()

atlas = sitk.ReadImage('atlas_resampled.mha')
image = sitk.ReadImage('brain2.mha')

# print(atlas)

elastix = sitk.SimpleElastix()
elastix.LogToConsoleOn()

elastix.SetFixedImage(atlas)
elastix.SetMovingImage(image)

# elastix.SetParameterMap(sitk.ReadParameterFile("rigid.txt"))
# elastix.Execute()
# result_rigid = elastix.GetResultImage()
# sitk.WriteImage(result_rigid, 'result_rigid2.nii')
# result_rigid = sitk.ReadImage("result_rigid2.nii")
#
# elastix.setMovingImage(result_rigid)
# elastix.SetParameterMap(sitk.ReadParameterFile('affine.txt'))
# elastix.Execute()
# result_affine = elastix.GetResultImage()
#
# sitk.WriteImage(result_affine, 'result_rigid_affine2.nii')
