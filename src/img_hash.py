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
        logging.warning(msg=f"{str(e)}")
        print("history is empty")
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
    found = 0

    # Ensure result is iterable
    if isinstance(result, list):
        for entry in result:
            for image_path_str, values in entry.items():
                if image_path_str == image_path:
                    # Cache current image results
                    current_image_results = values.get("image_results", [])

                    # Compare against previous history
                    try:
                        if len(history_json) > 0:
                            for entry in history_json:
                                try:
                                    history_image_hash = generate_phash(
                                        entry["image"])
                                except Exception:
                                    continue
                                if history_image_hash is None:
                                    continue
                                if (history_image_hash - hash_image_path) in range(10):
                                    found = 1
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
                                    # automatic metadata id update
                                    entry["id"] = values.get(
                                        "search_metadata_id", "")
                                    break
                            if not found:
                                old_links = current_image_results
                                # append new data set
                                history_json.append(append_archive_data(
                                    image_path_str, values.get("search_metadata_id", "")))
                                # save to history & break
                                history_to_file = json.dumps(
                                    history_json, indent=4)
                                try:
                                    with open("./results/history.json", "w", encoding="utf-8") as file:
                                        file.write(history_to_file)
                                except (json.JSONDecodeError, FileNotFoundError) as e:
                                    logging.error(msg=f"{str(e)}")
                                    print("Failed to update history.json")
                        else:
                            old_links = current_image_results
                            # append new data set
                            history_json.append(append_archive_data(
                                image_path_str, values.get("search_metadata_id", "")))
                            # save to history & break
                            history_to_file = json.dumps(
                                history_json, indent=4)
                            try:
                                with open("./results/history.json", "w", encoding="utf-8") as file:
                                    file.write(history_to_file)
                            except (json.JSONDecodeError, FileNotFoundError) as e:
                                logging.error(msg=f"{str(e)}")
                                print("Failed to update history.json")

                    except Exception as e:
                        logging.error(f"Error retrieving archived data: {e}")
                        continue

        # Return sorted results
        output = {"old": old_links, "new": new_links}
        return output
    else:
        logging.error("Result is not a list. Cannot process data.")


def append_archive_data(image_path: str, id: str) -> dict:
    return {
        "image": image_path,
        "id": id
    }


if __name__ == "__main__":
    archive_processor(
        "C:\\Users\\StarGate\\Documents\\TraceIt\\data\\images\\Venom_FA.webp")
