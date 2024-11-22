from PIL import Image
import imagehash
from img_processor import image_processor
import json
from pprint import pprint
import requests
from dotenv import find_dotenv, load_dotenv
import os
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

# add result dic


def archive_processor() -> dict:
    new_data = []
    result = None
    with open("./results/reverse_image_search_results.json", "r", encoding="utf-8") as file:
        result = json.load(file)
    # read from history file
    history_json = None
    with open("./results/history.json", "r", encoding="utf-8") as file:
        history_json = json.load(file)

    for entry in result:
        for imagepath_key, values in entry.items():
            id = compare(image_path_key=imagepath_key,
                         history_json=history_json)
            if id:
                print("ok")
                archive_image_list = get_archive(id)
                current_image_list = values["image_results"]
                new_link = [
                    val for val in archive_image_list if val not in current_image_list]

                pprint(f"this are the archive_image_list links: {
                       archive_image_list}")
                pprint(f"this are the current_image_list links: {
                       current_image_list}")
                pprint(f"this are the new links: {new_link}")
            else:
                new_data.append(
                    {
                        "image": imagepath_key,
                        "id": values["search_metadata_id"]
                    }
                )
    pprint(new_data)

    to_json = json.dumps(new_data, indent=4)
    with open("./results/history.json", "w", encoding="utf-8") as file:
        file.write(to_json)
    # save this to json file


def compare(image_path_key: str, history_json: dict) -> bool:
    current_image_hash = generate_phash(image_path_key)
    for entry in history_json:
        history_hash = generate_phash(entry["image"])
        if (current_image_hash - history_hash) in range(10):
            return entry["id"]
    return False


def get_archive(id) -> dict:
    envpath = find_dotenv()

    if not load_dotenv(envpath):
        raise EnvironmentError(
            "No .env file found or failed to load environment variables.")

    search_id = id
    response = requests.get(
        f"https://serpapi.com/searches/{search_id}.json", params={"api_key": os.getenv("SERPAPI_KEY")}, timeout=10)
    response = response.json()
    image_result = [entry["link"] for entry in response["image_results"]]
    return image_result


if __name__ == "__main__":
    archive_processor()
