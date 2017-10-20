import SimpleITK as sitk

filename = r"NCCT_FIRST_FEW\R0005\26175551\1.3.6.1.4.1.40744.9.296714357679029894627575101190395137849.mha"

result = sitk.ReadImage(filename)
print(result)
print(result.GetSize()[-1])
