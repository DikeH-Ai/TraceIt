import inquirer
from pprint import pprint
import time
import threading
from pynput.keyboard import Controller, Key
from rapidfuzz import process, fuzz
import json


def set_timer(answer: list, default: bool):
    """
        Automatic input after 7 seconds without a user input
        failsafe for autonomous operation
    """
    try:
        time.sleep(7)
        if answer[0] == None:
            print(f"\nTimeout! Using default answer")
            answer[0] = default
            # press Enter key
            keyboard_controller = Controller()
            keyboard_controller.press(Key.enter)
            keyboard_controller.release(Key.enter)
    except Exception as e:
        print(f"An error has occured(func: set_timer): {str(e)}")


def question_timer() -> bool:
    """
        Modify user settings-> True or False
    """
    try:
        question = [
            inquirer.Confirm("setup", message="Set custom parameters")
        ]
        answers = [None]
        # using another process to call the timer
        timer_thread = threading.Thread(
            target=set_timer, args=(answers, False))
        timer_thread.daemon = True
        # start function
        timer_thread.start()

        # response is assinged to ans
        ans = inquirer.prompt(question)
        # if user response before the timer runs down
        if ans:
            answers[0] = ans["setup"]

        return answers[0]
    except Exception as e:
        print(f"An error has occured(func: question_timer): {str(e)}")


def custom_parameters() -> dict:
    """
        Setup;
            "Geographic Location":
            "Localization":,
            "Pagination":,
            "Advanced Parameters":,
            "Advanced Filters":,
            "SerpApi Parameters":
        settings
    """
    try:
        # each function dictionary holder
        func_dict = {
            "Geographic Location": geo_location,
            "Localization": localization,
            # "Pagination":,
            # "Advanced Parameters":,
            # "Advanced Filters":,
            # "SerpApi Parameters":
        }
        # parameters

        parameters = {
            "engine": "google_reverse_image",
            "image_url": None,
            "api_key": "secret_api_key"
        }
        while True:
            question = [
                inquirer.List("settings",
                              message="Select Settings",
                              choices=["Geographic Location", "Localization", "Pagination", "Advanced Parameters", "Advanced Filters", "SerpApi Parameters", "Exit"]),
            ]
            answers = inquirer.prompt(question)

            if answers["settings"] == "Exit":
                print("Exiting Custom settings")
                break
            else:
                pprint(answers)
                data = func_dict[answers["settings"]]()
                if data:
                    parameters.update(data)
        return parameters
    except Exception as e:
        print(f"An error has occured(func: custom_parameters): {str(e)}")


def default_parameters() -> dict:
    """
        Use the default query parameters
    """
    parameters = {
        "engine": "google_reverse_image",
        "image_url": None,
        "api_key": "secret_api_key"
    }
    print("In default")
    return parameters


"""
    Each custom settings
"""


def geo_location() -> dict:
    try:
        while True:
            question = [
                inquirer.List('option', message="Select Settings (The location and uule parameters can't be used together)",
                              choices=["location", "uule", "Go back"])
            ]
            answers = inquirer.prompt(question)

            if answers["option"] == "location":
                return loaction_geo_location()
            elif answers["option"] == "Go back":
                break
            else:
                questions = [
                    inquirer.Text('uule',
                                  message="Input uule: "),
                ]

                uule_dict = inquirer.prompt(questions)
                return uule_dict
    except Exception as e:
        print(f"An error has occured(func: geo_location): {str(e)}")
        return

# location function in geo_location menu


def loaction_geo_location() -> dict:
    # get location list
    locations = []
    with open("./data/locations_list.txt", "r",  encoding="utf-8") as file:
        locations = file.readlines()
    locations = [location.strip() for location in locations]

    question1 = [
        inquirer.Text(
            'location', message="Location", default=None)
    ]

    input_text = inquirer.prompt(question1)
    matches = get_top_matches(
        # sort based on token ratio
        input_text["location"], locations, filter=fuzz.token_sort_ratio)
    matches = [match[0] for match in matches]
    matches.append(None)
    question2 = [
        inquirer.List(
            'location', message="Select Location", choices=matches)
    ]

    selected_loc = inquirer.prompt(question2)
    if selected_loc["location"]:
        return selected_loc

# Function to get the top 10 closest matches using rapidwuzzy


def get_top_matches(user_input, location_list, filter=None, top_n=10):
    if filter:
        matches = process.extract(
            user_input, location_list, limit=top_n, scorer=filter)
        return matches
    else:
        matches = process.extract(user_input, location_list, limit=top_n)
        return matches


def localization() -> dict:
    try:
        while True:
            # stage 2 menu
            question = [
                inquirer.List("options", message="Select settings", choices=[
                              "Domain", "Country", "Language", "Set Multiple Languages", "Go back"])
            ]
            answer = inquirer.prompt(question)

            if answer["options"] == "Domain":
                return localization_domain()
            elif answer["options"] == "Country":
                return localization_country()
            elif answer["options"] == "Language":
                pass
            elif answer["options"] == "Set Multiple Languages":
                question4 = [
                    inquirer.Text(
                        "multi-lan", message="Specify languages and | as a delimiter. (e.g., lang_fr|lang_de will only search French and German pages.")
                ]
                multi_lan = inquirer.prompt(question4)
                return multi_lan
            else:
                break
    except Exception as e:
        print(f"An error has occured(func: localization): {str(e)}")
        return

# domain function in the localization menu


def localization_domain() -> dict:
    # read domain list from google_domain.txt
    domains = []
    with open("./data/google_domains.txt", "r",  encoding="utf-8") as file:
        domains = file.readlines()
    domains = [domain.strip() for domain in domains]  # clean list
    # question1
    question1 = [
        inquirer.Text(
            "domain", message="Input domain(eg. google.ae) or List(to see all domains)")
    ]
    answer1 = inquirer.prompt(question1)
    # if List is typed
    if answer1["domain"].lower() == "list":
        question1b = [
            inquirer.List(
                "domain", message="pick a domain", choices=domains)
        ]
        answer1b = inquirer.prompt(question1b)
        if answer1b["domain"]:
            return set_parameter(answer1b)
    # compare answer to list
    matches = get_top_matches(answer1["domain"], domains)
    matches = [match[0] for match in matches]  # top 5 matches
    matches.append(None)  # append None option for exit feature
    # pick the right domain
    question1a = [
        inquirer.List(
            "domain", message="Pick a domain", choices=matches)
    ]
    answer1a = inquirer.prompt(question1a)
    # auto set parameter
    if answer1a["domain"]:
        return set_parameter(answer1a)

# auto set parameters for associated values


def set_parameter(option: dict) -> dict:
    data = None
    with open("./data/google-domains.json", "r", encoding="utf8") as file:
        data = json.load(file)
    for dict in data:
        if option["domain"] in dict.values():  # auto assign associated values
            para = {
                "google_domain": option["domain"],
                "gl": dict["country_code"],
                "hl": dict["language_code"]
            }
            print(para)
            return para


def localization_country() -> dict:
    pass


if __name__ == "__main__":
    choice = question_timer()
    pprint(choice)
    if choice:
        parameters = custom_parameters()
    else:
        parameters = default_parameters()
    print(parameters)
    # result_json = serp_search(parameters)
