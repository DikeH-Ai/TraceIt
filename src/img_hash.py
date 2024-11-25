from PIL import Image
import imagehash
from img_processor import image_processor
import json
from pprint import pprint
import requests
from dotenv import find_dotenv, load_dotenv
import os
import logging
import logging
import time
logger = logging.getLogger(__name__)
logging.basicConfig(filename='program.log',
                    encoding='utf-8', level=logging.DEBUG)
"""
Hash images and compare for similarity
"""


def generate_phash(image_path: str):
    """generate image hash for image comparison

    Args:
        image_path (str): relative image path
    """
    try:
        image = Image.open(image_path)
        return imagehash.phash(image)
    except Exception as e:
        logging.error(f"Error generating phash: {e}")
        return None


def archive_processor(image_path) -> dict:
    """extract & sort image result list into new and old
    link results

    Args:
        image_path str: file(file path)

    Returns:
        dict: {old:[], new:[]}
    """
    # generate search image hash
    hash_image_path = generate_phash(image_path=image_path)

    # compare to archive searched images
    # read from history
    try:
        with open("./results/history.json", "r", encoding="utf-8") as file:
            history_json = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logging.error(msg=f"{str(e)}")
        history_json = []
    # open result data to extract and sort data

    try:
        with open("./results/reverse_image_search_results.json", "r", encoding="utf-8") as file:
            result = json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        logging.error(msg=f"{str(e)}")
        result = []

    # if archive history is empty, nothig to compare
    # just append new history data
    # exit
    # Initialize placeholders
    new_links = []
    old_links = []

    # Ensure result is iterable
    if isinstance(result, list):
        for entry in result:
            for image_path_str, values in entry.items():
                if image_path_str == image_path:
                    # Cache current image results
                    current_image_results = values.get("image_results", [])

                    # Compare against previous history
                    try:
                        for entry in history_json:
                            history_image_hash = generate_phash(entry["image"])
                            if (history_image_hash - hash_image_path) in range(10):
                                # Fetch archived data
                                search_id = entry["id"]
                                response = requests.get(
                                    f"https://serpapi.com/searches/{
                                        search_id}.json",
                                    params={"api_key": os.getenv(
                                        "SERPAPI_KEY")},
                                    timeout=10
                                )
                                response.raise_for_status()  # Raise exception for HTTP errors
                                archive_data = response.json()
                                archived_image_results = [
                                    entry["link"] for entry in archive_data.get("image_results", [])
                                ]

                                # Sort links into "new" and "old"
                                old_links = archived_image_results
                                new_links = [
                                    link for link in current_image_results if link not in old_links
                                ]
                                break
                    except Exception as e:
                        logging.error(f"Error retrieving archived data: {e}")
                        continue

        # Return sorted results
        output = {"old": old_links, "new": new_links}
        return output
    else:
        logging.error("Result is not a list. Cannot process data.")


if __name__ == "__main__":
    archive_processor("./data/images\\pexels-photo-4238994.webp")
# add result dic


# def archive_processor(imageer_path) -> dict:
#     try:
#         result = None
#         with open("./results/reverse_image_search_results.json", "r", encoding="utf-8") as file:
#             result = json.load(file)
#         read from history file
#         history_json = []
#         try:
#             with open("./results/history.json", "r", encoding="utf-8") as file:
#                 history_json = json.load(file)
#         except json.JSONDecodeError:
#             pass
#         if history is empty add data and exit -- impliment
#         if history_json:
#             for entry in result:
#                 for imagepath_key, values in entry.items():
#                     if imagepath_key == imageer_path:
#                         id = compare(image_path_key=imagepath_key,
#                                      history_json=history_json)
#                         if id:
#                             print("ok")
#                             archive_image_list = get_archive(id)
#                             current_image_list = values["image_results"]
#                             new_link = [
#                                 val for val in archive_image_list if val not in current_image_list]

#                             pprint(f"this are the archive_image_list links: {
#                                 archive_image_list}")
#                             pprint(f"this are the current_image_list links: {
#                                 current_image_list}")
#                             pprint(f"this are the new links: {new_link}")
#                             if len(new_link) > 0:
#                                 update_historyjson(
#                                     history_json, imagepath_key, values["search_metadata_id"])
#                             return new_link
#                         else:
#                             history_json.append(
#                                 {
#                                     "image": imagepath_key,
#                                     "id": values["search_metadata_id"]
#                                 }
#                             )
#                             retu
#                     else:
#                         return None
#         else:
#             for entry in result:
#                 for imagepath_key, values in entry.items():
#                     history_json.append(
#                         {
#                             "image": imagepath_key,
#                             "id": values["search_metadata_id"]
#                         }
#                     )
#         history_json = json.dumps(history_json, indent=4)
#         with open("./results/history.json", "w", encoding="utf-8") as file:
#             file.write(history_json)
#         return None
#     except Exception as e:
#         print(f"An error has occured(func: archive_processor): {str(e)}")


# def update_historyjson(historyjson: list, image_path_key: str, id: str) -> None:
#     try:
#         for entry in historyjson:
#             if entry["image"] == image_path_key:
#                 entry["id"] = id
#         with open("./results/history.json", "w", encoding="utf-8") as file:
#             file.write(historyjson)
#     except Exception as e:
#         print(f"An error has occured(func: update_historyjson): {str(e)}")


# def compare(image_path_key: str, history_json: dict) -> bool:
#     try:
#         current_image_hash = generate_phash(image_path_key)
#         for entry in history_json:
#             history_hash = generate_phash(entry["image"])
#             if (current_image_hash - history_hash) in range(10):
#                 return entry["id"]
#         return False
#     except Exception as e:
#         print(f"An error has occured(func: compare): {str(e)}")


# def get_archive(id) -> dict:
#     try:
#         envpath = find_dotenv()

#         if not load_dotenv(envpath):
#             raise EnvironmentError(
#                 "No .env file found or failed to load environment variables.")

#         search_id = id
#         response = requests.get(
#             f"https://serpapi.com/searches/{search_id}.json", params={"api_key": os.getenv("SERPAPI_KEY")}, timeout=10)
#         response = response.json()
#         image_result = [entry["link"] for entry in response["image_results"]]
#         return image_result
#     except Exception as e:
#         print(f"An error has occured(func: get_archive): {str(e)}")
