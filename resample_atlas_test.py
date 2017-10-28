import SimpleITK as sitk

atlas = sitk.ReadImage("atlas.mha")
image = sitk.ReadImage("D:\Geert\SOFT_TISSUE_THICK\R0002.mha")
interpolator = sitk.sitkLinear
# interpolator = sitk.sitkBSpline


resampler = sitk.ResampleImageFilter()
# resampler.SetReferenceImage(image)


resampler.SetInterpolator(interpolator)
resampler.SetTransform(sitk.Transform())

resampler.SetSize(image.GetSize())
resampler.SetOutputSpacing(image.GetSpacing())
# resampler.SetOutputOrigin(image.GetOrigin())
resampler.SetOuputDirection(image.GetDirection())
# resampled_atlas = resampler.Execute(atlas)
print( resampler.GetOutputOrigin() )

sitk.WriteImage(resampled_atlas, "resampled_atlas.mha")
