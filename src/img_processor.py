import os
import filetype  # type: ignore
import sys
import cloudinary  # type: ignore
import cloudinary.uploader  # type: ignore
from dotenv import find_dotenv, load_dotenv  # type: ignore


def main():
    imagepaths = image_processor()
    image_dict = upload_to_cloudinary(imagepaths=imagepaths)
    print(image_dict)
    delete_image(image_dict)


def is_image(filepath: str) -> bool:  # get file format
    """
        Checks if file is an image
    """
    try:
        file_kind = filetype.guess(filepath)
        if file_kind is not None and file_kind.mime.startswith('image/'):
            return True
        return False
    except Exception:
        return False


def image_processor() -> list:
    """
        return imagepath list
    """
    try:
        # Access image folder
        image_path = "./data/images"
        images = os.listdir(image_path)  # get images
        # validate images
        images = [os.path.join(image_path, image) for image in images if is_image(
            os.path.join(image_path, image))]
        return images
    except Exception as e:
        print(f"Image processing failed {str(e)}", file=sys.stderr)
        return []


def upload_to_cloudinary(imagepaths: list) -> dict:
    """
        Handles Api request to cloudinary
        Converts images to url links
        You will require an account with https://cloudinary.com/
        Set up enviroment variables for config tokens
    """
    # get env variable
    dotenv_path = find_dotenv()

    if not imagepaths and load_dotenv:  # quit app if no image is found
        sys.exit("No image found")

    if not load_dotenv(dotenv_path):
        print("Warning: No config data setup in environment variable")
    # cloudinary config
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
    )

    # image upload
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
            print(f"Failed to upload {image}: {str(e)}")
    return images_dict


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
                print(f"Image with public_id {
                    public_id} deleted successfully.")
            else:
                print(f"Failed to delete image with public_id {
                    public_id}: {response}")
    except Exception as e:
        # Catch and print any exceptions that occur during deletion
        print(f"Error deleting image with public_id {public_id}: {str(e)}")


if __name__ == "__main__":
    main()
