import SimpleITK as sitk
import math
import os
import numpy as np

#============ FOR CTA ============
# Radius (in mm) of biggest hole in the skull after the foramen magnum.
#FORAMEN_RADIUS_IN_MM = 7

#MIN_SKULL_HU_VALUE = 350
#MAX_BRAIN_HU_VALUE = 330
#MIN_BRAIN_HU_VALUE = -20

#============ FOR NCCT ============
FORAMEN_RADIUS_IN_MM = 7

MIN_SKULL_HU_VALUE = 160
MAX_BRAIN_HU_VALUE = 140
MIN_BRAIN_HU_VALUE = -20

INPUT_FOLDER = "D:\Geert\SOFT_TISSUE_THICK_REGISTERED"
INPUT_FILE = os.path.join(INPUT_FOLDER, "soft_tissue_thick_registered.txt")
OUTPUT_FOLDER = "D:\Geert\SOFT_TISSUE_THICK_SKULL_STRIPPED"

already_processed_scans = os.listdir(OUTPUT_FOLDER)


def crop(image):
    """
    Crops zero padding after brain mask has been applied.
    """
    image_array = sitk.GetArrayFromImage(image)
    if np.all(image_array == 0):
        return []

    for i in range(image_array.ndim):
        image_array = np.swapaxes(image_array, 0, i)  # send i-th axis to front
        while np.all(image_array[0] == 0):
            image_array = image_array[1:]
        while np.all(image_array[-1] == 0):
            image_array = image_array[:-1]
        image_array = np.swapaxes(image_array, 0, i)  # send i-th axis to its original position
    return sitk.GetImageFromArray(image_array)


if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

with open(INPUT_FILE) as input_file:
    for line in input_file:

        new_line = line.replace("\n", "")
        if new_line in already_processed_scans:
            print("skipping {}, already exists in output folder.".format(new_line))
            continue

        print("Start processing {0}.".format(new_line))

        input_image = sitk.ReadImage(os.path.join(INPUT_FOLDER, new_line))

        FORAMEN_RADIUS_3D = (math.floor(FORAMEN_RADIUS_IN_MM / input_image.GetSpacing()[0]),
                             math.floor(FORAMEN_RADIUS_IN_MM / input_image.GetSpacing()[1]),
                             math.floor(FORAMEN_RADIUS_IN_MM / input_image.GetSpacing()[2]))

        # Segment all bone in the image.
        aux_image = input_image > MIN_SKULL_HU_VALUE

        # Bring values for the scale from 0 to 1 (0 is background and 1 is the foreground).
        clamp = sitk.ClampImageFilter()
        clamp.SetLowerBound(0)
        clamp.SetUpperBound(1)
        aux_image = clamp.Execute(aux_image)
        aux_image = sitk.Cast(aux_image, sitk.sitkInt32)

        # Close skull holes
        dilate = sitk.BinaryDilateImageFilter()
        dilate.SetBackgroundValue(0)
        dilate.SetForegroundValue(1)
        dilate.SetKernelRadius(FORAMEN_RADIUS_3D)
        aux_image = dilate.Execute(aux_image)
        skull_without_holes = aux_image

        # Segment area outside the skull. Also finds the slice with seed for brain segmentation inside the skull.
        slice_id = input_image.GetSize()[2] - 1
        while slice_id >= 0:
            aux_slice = aux_image[:, :, slice_id]

            region_growing_filter = sitk.ConnectedThresholdImageFilter()
            region_growing_filter.SetLower(0)
            region_growing_filter.SetUpper(0)
            region_growing_filter.SetSeed([0, 0])

            slice_mask = region_growing_filter.Execute(aux_slice)
            slice_mask = sitk.Cast(slice_mask, aux_image.GetPixelID())
            slice_mask = sitk.JoinSeries(slice_mask)

            aux_image = sitk.Paste(aux_image, slice_mask, slice_mask.GetSize(), destinationIndex = [0, 0, slice_id])
            slice_id = slice_id - 1

        # Dilate the segmentation of the area outside the skull back to the skull border.
        outside_skull_mask = dilate.Execute(aux_image)
        outside_skull_mask.SetOrigin(input_image.GetOrigin())
        outside_skull_mask.SetDirection(input_image.GetDirection())
        outside_skull_mask.SetSpacing(input_image.GetSpacing())

        # Save intermediate result. TODO: To be removed.
        #sitk.WriteImage(outside_skull_mask, "C:/Users/renan/Downloads/outside_skull_mask.mha")
        #sitk.WriteImage(skull_without_holes, "C:/Users/renan/Downloads/skull_without_holes.mha")

        # Remove other connected components that are not part of the brain.
        outside_brain_mask = outside_skull_mask + skull_without_holes
        outside_brain_mask = sitk.Clamp(outside_brain_mask, lowerBound = 0, upperBound = 1)
        outside_brain_mask = sitk.Cast(outside_brain_mask, sitk.sitkInt32)
        outside_brain_mask = sitk.InvertIntensity(outside_brain_mask, 1)
        outside_brain_mask = sitk.Cast(outside_brain_mask, sitk.sitkInt32)
        outside_brain_mask = sitk.RelabelComponent(sitk.ConnectedComponent(outside_brain_mask))
        outside_brain_mask = sitk.Threshold(outside_brain_mask)

        # Dilate the segmentation of the area inside the skull back to the skull border.
        outside_brain_mask = dilate.Execute(outside_brain_mask)
        outside_brain_mask = sitk.InvertIntensity(outside_brain_mask, 1)
        outside_brain_mask = sitk.Cast(outside_brain_mask, sitk.sitkInt32)

        # Save intermediate result. TODO: To be removed.
        #sitk.WriteImage(outside_brain_mask, "C:/Users/renan/Downloads/outside_brain_mask.mha")

        # Finds slice with biggest portion of brain.

        previous_area = -1
        previous_slice_id = -1
        slices_where_area_trend_change = []
        slice_id = input_image.GetSize()[2] - 1
        while slice_id >= 0:
            slice_mask = outside_brain_mask[:, :, slice_id]
            slice_mask = sitk.Cast(slice_mask, sitk.sitkInt32)
            label_info_filter = sitk.LabelStatisticsImageFilter()
            label_info_filter.Execute(slice_mask, slice_mask)
            if previous_area == -1:
                previous_area = label_info_filter.GetCount(0)
                previous_slice_id = slice_id
            else:
                current_area = label_info_filter.GetCount(0)
                if abs(current_area - previous_area) > 0.05 * (current_area if current_area < previous_area else previous_area):
                    if current_area < previous_area:
                        slices_where_area_trend_change.append(previous_slice_id)
                previous_area = current_area
                previous_slice_id = slice_id
            slice_id = slice_id - 1

        # HU value of air + threshold to account for noise + value to stay above the max brain HU value.
        HU_DELTA = 1000 + 100 + (MAX_BRAIN_HU_VALUE + abs(MIN_BRAIN_HU_VALUE))
        aux_image = outside_brain_mask * HU_DELTA + sitk.Cast(input_image, sitk.sitkInt32)
        aux_image = sitk.Cast(aux_image, sitk.sitkInt32)

        # Save intermediate result. TODO: To be removed.
        #sitk.WriteImage(aux_image, "C:/Users/renan/Downloads/region_growing_input.mha")

        #Get a seed inside the brain
        slice_with_big_brain_area_number = 0
        if len(slices_where_area_trend_change) != 0:
            slice_with_big_brain_area_number = slices_where_area_trend_change[0]

        slice_with_big_brain_area = outside_brain_mask[:, :, slice_with_big_brain_area_number]
        slice_with_big_brain_area = sitk.InvertIntensity(slice_with_big_brain_area, 1)
        slice_info = sitk.LabelStatisticsImageFilter()
        slice_info.Execute(slice_with_big_brain_area, slice_with_big_brain_area)
        bound_box = slice_info.GetBoundingBox(1)
        seed_x = int((bound_box[1]-bound_box[0])/2 + bound_box[0])
        seed_y = int((bound_box[3]-bound_box[2])/2 + bound_box[2])
        seed = (seed_x, seed_y, slice_with_big_brain_area_number)

        # Use region growing inside the brain
        region_growing_filter = sitk.ConnectedThresholdImageFilter()
        region_growing_filter.SetLower(MIN_BRAIN_HU_VALUE)
        region_growing_filter.SetUpper(MAX_BRAIN_HU_VALUE)
        region_growing_filter.SetSeed(seed)
        aux_image = region_growing_filter.Execute(aux_image)
        aux_image = sitk.BinaryFillhole(aux_image)
        aux_image = sitk.Cast(aux_image, sitk.sitkUInt8)

        # Save intermediate result. TODO: To be removed.
        #sitk.WriteImage(aux_image, "C:/Users/renan/Downloads/skull stripping validation data/region_growing_output.mha")

        FINAL_KERNEL = (math.floor(1 / input_image.GetSpacing()[0]),
                        math.floor(1 / input_image.GetSpacing()[1]),
                        math.floor(1 / input_image.GetSpacing()[2]))
        erode = sitk.BinaryErodeImageFilter()
        erode.SetForegroundValue(1)
        erode.SetBackgroundValue(0)
        erode.SetKernelRadius(FINAL_KERNEL)

        aux_image = erode.Execute(aux_image)

        FINAL_KERNEL = (math.floor(2 / input_image.GetSpacing()[0]),
                        math.floor(2 / input_image.GetSpacing()[1]),
                        math.floor(2 / input_image.GetSpacing()[2]))
        dilate = sitk.BinaryDilateImageFilter()
        dilate.SetForegroundValue(1)
        dilate.SetBackgroundValue(0)
        dilate.SetKernelRadius(FINAL_KERNEL)

        aux_image = dilate.Execute(aux_image)
        aux_image = erode.Execute(aux_image)

        # Segment all bone in the image but now using the brain threshold.
        bone_mask = input_image > MAX_BRAIN_HU_VALUE

        # Bring values for the scale from 0 to 1 (0 is background and 1 is the foreground).
        clamp = sitk.ClampImageFilter()
        clamp.SetLowerBound(0)
        clamp.SetUpperBound(1)
        bone_mask = clamp.Execute(bone_mask)
        bone_mask = sitk.Cast(bone_mask, sitk.sitkInt32)

        aux_image = sitk.Cast(aux_image, sitk.sitkInt32)

        aux_image = aux_image - bone_mask
        aux_image = clamp.Execute(aux_image)
        aux_image = sitk.Cast(aux_image, sitk.sitkInt32)

        aux_image = sitk.RelabelComponent(sitk.ConnectedComponent(aux_image))
        aux_image = sitk.Threshold(aux_image)
        aux_image = sitk.BinaryFillhole(aux_image)

        # aux_image = sitk.Cast(aux_image, sitk.sitkUInt8)
        aux_image = sitk.Cast(aux_image, sitk.sitkInt16)
        # multiply by mask to get skull stripped image and crop
        import pdb; pdb.set_trace()
        skull_stripped_image = crop(aux_image * input_image)


        if skull_stripped_image:
            # Save final result
            sitk.WriteImage(skull_stripped_image, os.path.join(OUTPUT_FOLDER, new_line))
            print("File {0} processed".format(new_line))
        else:
            print("{} couldn't be processed: the mask gave all zeroes.".format(new_line))
