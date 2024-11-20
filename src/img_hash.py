from PIL import Image
import imagehash
from img_processor import image_processor
import json
"""
Hash images and compare for similarity
"""


def main():
    imagepath_list = image_processor()
    for imgpath in imagepath_list:
        print(generate_phash(image_path=imgpath))


def generate_phash(image_path: str):
    """generate image hash for image comparison

    Args:
        image_path (str): relative image path 
    """
    image = Image.open(image_path)
    return imagehash.phash(image)


if __name__ == "__main__":
    main()
