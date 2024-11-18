import json

"""
    Clean data
"""


def main():
    data = None
    with open("./data/default_parameter.json", "r", encoding="utf8") as file:
        data = json.load(file)
    print(data)
    # languages = [lan["language_name"] for lan in data]
    # with open("./data/google_languages.txt", "w", encoding="utf-8") as file:
    #     file.write("\n".join(languages))
    # languages = []
    # with open("./data/google_languages.txt", "r",  encoding="utf-8") as file:
    #     languages = file.readlines()
    # languages = [language.strip() for language in languages]
    # print(languages)
    # data = None
    # with open("./data/google-domains.json", "r", encoding="utf8") as file:
    #     data = json.load(file)
    # for dict in data:
    #     if 'google.tk' in dict.values():
    #         print(dict)


if __name__ == "__main__":
    main()
