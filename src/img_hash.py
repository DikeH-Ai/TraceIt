from PIL import Image
import imagehash
from img_processor import image_processor
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


def archive_processor(result: dict) -> dict:
    new_data = {}
    # extract imagepath, search_metadata.id, image_result
    for entry in result:
        for result_key, result_value in result.items():
            himage_path = generate_phash(result_key)


if __name__ == "__main__":
    main()
