import json

"""
    Clean data
"""


def main():
    data = None
    with open("./data/locations.json", "r", encoding="utf8") as file:
        data = json.load(file)

    locations = [loc["canonical_name"] for loc in data]
    with open("./data/locations_list.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(locations))
    locations = []
    with open("./data/locations_list.txt", "r",  encoding="utf-8") as file:
        locations = file.readlines()
    locations = [location.strip() for location in locations]


if __name__ == "__main__":
    main()
