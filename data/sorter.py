import json

"""
    Clean data
"""


def main():
    data = None
    with open("./data/google-domains.json", "r", encoding="utf8") as file:
        data = json.load(file)

    countries = [con["country_name"] for con in data]
    with open("./data/google_country.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(countries))
    countries = []
    with open("./data/google_country.txt", "r",  encoding="utf-8") as file:
        countries = file.readlines()
    countries = [country.strip() for country in countries]
    print(countries)
    # data = None
    # with open("./data/google-domains.json", "r", encoding="utf8") as file:
    #     data = json.load(file)
    # for dict in data:
    #     if 'google.tk' in dict.values():
    #         print(dict)


if __name__ == "__main__":
    main()
