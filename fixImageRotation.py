#
# fixImageRotation.py - A script to fix image rotation based on EXIF data
#
# (C) 2023 Marcel Verpaalen
#
# Licensed under the GNU GPL v3.0 license
#

import os

import pyexiv2
from PIL import Image, ImageOps


def fix_exif_data(imagefile):
    """
    Fixes the EXIF data of an image file to set the orientation to 1.

    Args:
        imagefile (str): The file path of the image to fix.

    Returns:
        None
    """
    with open(imagefile, "rb+") as f:
        with pyexiv2.ImageData(f.read()) as img:
            exif = img.read_exif()
            print(exif)

            img.modify_exif({"Exif.Image.Orientation": 1})
            # Empty the original file
            f.seek(0)
            f.truncate()
            # Get the bytes data of the image and save it to the file
            f.write(img.get_bytes())


def get_orientation_description(orientation):
    """
    Returns a string description of the given image orientation code.

    Parameters:
    orientation (int): An integer representing the image orientation code.

    Returns:
    str: A string description of the given image orientation code.
    """
    orientation_descriptions = {
        1: "Normal",
        2: "Flipped horizontally",
        3: "Upside down",
        4: "Flipped vertically",
        5: "Rotated 90 degrees counterclockwise and flipped horizontally",
        6: "Rotated 90 degrees counterclockwise",
        7: "Rotated 90 degrees counterclockwise and flipped vertically",
        8: "Rotated 90 degrees clockwise",
    }
    return orientation_descriptions.get(orientation, "Unknown")


def fix_image_rotation(image_path):
    """
    Rotates an image based on its EXIF orientation tag and saves it with orientation tag set to 1.

    Args:
        image_path (str): The file path of the image to be rotated.

    Returns:
        None
    """
    img = Image.open(image_path)

    exif = img.getexif()

    if exif:
        # 274 corresponds to the 'Orientation' tag, default to 1 if not found
        orientation = exif.get(274, 1)
        orientation_description = get_orientation_description(orientation)

        # Get image dimensions (width and height)
        width, height = img.size

        print(f"Original Orientation: {orientation} - {orientation_description}")
        print(f"Dimensions: {width} x {height}")

        if orientation > 1:
            image = ImageOps.exif_transpose(img)

            # Remove the EXIF orientation tag (set it to 1) --> Does not work, not saved
            exif[274] = 1  # 274 corresponds to the 'Orientation' tag
            image.save(image_path, exif=img.info["exif"])
            fix_exif_data(image_path)
            print("Rotated to Orientation 1")
        print()
    else:
        print("No EXIF data found.\n")


def rotate_images(folder_path):
    """
    Rotates all JPEG images in the specified folder to the correct orientation.

    Args:
        folder_path (str): The path to the folder containing the images to be rotated.
    """
    files = os.listdir(folder_path)
    files.sort()
    for file in files:
        if file.endswith(".jpg"):
            file_path = os.path.join(folder_path, file)
            fix_image_rotation(file_path)


# rotate_images("C:\\TMP\Photo")
rotate_images("D:\\")
