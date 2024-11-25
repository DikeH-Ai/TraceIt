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
