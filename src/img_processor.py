import os
import filetype
import sys
import cloudinary
import cloudinary.uploader
from dotenv import find_dotenv, load_dotenv
import logging


def main():
    imagepaths = image_processor()
    image_dict = upload_to_cloudinary(imagepaths=imagepaths)
    print(image_dict)
    delete_image(image_dict)
    pass


def is_image(filepath: str) -> bool:  # get file format
    """checks if file is an image

    Args:
        filepath (str): filepath

    Returns:
        bool: True|False
    """
    try:
        # using the filetype module
        file_kind = filetype.guess(filepath)
        # returns true if file is an image
        if file_kind is not None and file_kind.mime.startswith('image/'):
            return True
        return False
    except Exception:  # returns false on error
        return False


def image_processor() -> list:
    """Return "image path" list, path to the image in local
    directory

    Returns:
        list: list[filepath, filepath1, ...]
    """
    try:
        # Access image folder
        image_path = "./data/images"
        files = os.listdir(image_path)  # get files
        # validate images and append to path list
        images = [os.path.join(image_path, image) for image in files if is_image(
            os.path.join(image_path, image))]
        return images
    except Exception as e:
        logging.warning(
            f"Image processing failed(func: image_processor) {str(e)}")
        return []


def upload_to_cloudinary(imagepaths: list) -> dict:
    """
        Handles Api request to cloudinary
        Converts images to url links
        You will require an account with https://cloudinary.com/
        Set up enviroment variables for config tokens
    """
    try:
        # get env variable
        dotenv_path = find_dotenv()

        if not imagepaths:  # quit app if no image is found
            sys.exit("No image found")

        if not load_dotenv(dotenv_path):  # if env not found
            logging.warning(
                "Warning: No config data setup in environment variable file (.env)")

        # cloudinary config
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
        )

        # image upload logic
        images_dict = {}
        for image in imagepaths:
            try:
                response = cloudinary.uploader.upload(image)
                if "error" in response:
                    raise Exception(f"response_error: {
                                    str(response["error"]["message"])}")
                images_dict[image] = {
                    "url": response["url"],
                    "public_id": response["public_id"]
                }
            except Exception as e:
                logging.warning(f"Failed to upload {image}: {str(e)}")
        return images_dict
    except Exception as e:
        logging.error(
            f"An error has occured (func: upload_to_cloudinary): {str(e)}")


def delete_image(image_dict: dict):
    """
        delete images from cloudinary
    """
    try:
        public_ids = [image_data["public_id"]
                      for image_data in image_dict.values()]
        for public_id in public_ids:
            response = cloudinary.uploader.destroy(public_id)

            # Check if the response contains a success status
            if response.get("result") == "ok":
                logging.info(f"Image with public_id {
                    public_id} deleted successfully.")
            else:
                logging.info(f"Failed to delete image with public_id {
                    public_id}: {response}")
    except Exception as e:
        # Catch and print any exceptions that occur during deletion
        logging.warning(f"Error deleting image with public_id {
                        public_id}: {str(e)}")


if __name__ == "__main__":
    main()
