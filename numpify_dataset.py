import SimpleITK as sitk
import numpy as np
import os


def read_folder_as_label(folder, label, image_arrays, labels):
    """
    Read folder of images as numpy arrays and append to list 'image_arrays' and
    append 'label' to list 'labels'.
    """
    for scan_path in os.listdir(folder):
        full_path = os.path.join(folder, scan_path)
        # Need to convert format from (z, y, x) to (x, y, z).
        image_array = np.swapaxes( sitk.GetArrayFromImage( sitk.ReadImage(full_path) ), 0, 2 )
        image_arrays.append(image_array)
        labels.append(label)


def concatenate_with_padding(list_of_arrays, padding=0):
    """
    Concatenates list of n numpy arrays to a single numpy array of shape
    (n, max_x, max_y, max_z) where max_x is the max([array.shape[0] for array in list_of_arrays]).
    Smaller arrays are padded with padding.
    """
    n = len(list_of_arrays)
    max_x = max(array.shape[0] for array in list_of_arrays)
    max_y = max(array.shape[1] for array in list_of_arrays)
    max_z = max(array.shape[2] for array in list_of_arrays)
    result = np.zeros((n, max_x, max_y, max_z))

    for i, array in enumerate(list_of_arrays):
        pad_x_left, pad_x_right = split_in_half(max_x - array.shape[0])
        pad_y_left, pad_y_right = split_in_half(max_y - array.shape[1])
        pad_z_left, pad_z_right = split_in_half(max_z - array.shape[2])
        padded_array = np.pad(
            array,
            ((pad_x_left, pad_x_right), (pad_y_left, pad_y_right), (pad_z_left, pad_z_right)),
            'constant',
            constant_values=padding)
        result[i, :, :, :] = padded_array

    return result


def split_in_half(integer):
    if integer % 2 == 0:
        return (integer // 2, integer // 2)
    else:
        return (integer // 2 + 1, integer // 2)


if __name__ == '__main__':
    INPUT_FOLDER = "D:\Geert\SOFT_TISSUE_THICK_DATASET_DOWNSAMPLED"
    AFFECTED_FOLDER = os.path.join(INPUT_FOLDER, "AFFECTED")
    UNAFFECTED_FOLDER = os.path.join(INPUT_FOLDER, "UNAFFECTED")
    OUTPUT_FOLDER = "D:\Geert\SOFT_TISSUE_THICK_DOWNSAMPLED_NUMPIFIED"
    AFFECTED = 1
    UNAFFECTED = -1

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    images = []
    labels = []
    read_folder_as_label(AFFECTED_FOLDER, AFFECTED, images, labels)
    read_folder_as_label(UNAFFECTED_FOLDER, UNAFFECTED, images, labels)
    dataset = concatenate_with_padding(images)
    labels = np.array(labels)

    np.save( os.path.join(OUTPUT_FOLDER, 'dataset.npy'), dataset)
    np.save( os.path.join(OUTPUT_FOLDER, 'labels.npy'), labels)
