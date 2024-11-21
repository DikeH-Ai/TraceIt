import inquirer
from pprint import pprint
import time
import threading
from pynput.keyboard import Controller, Key
from rapidfuzz import process, fuzz
import json
from dotenv import find_dotenv, load_dotenv
from os import getenv
from serpapi import GoogleSearch


def set_timer(answer: list, default: bool):
    """    Sets a timer to automatically assign a default boolean value to the 
    provided `answer` list if no user input is received within 7 seconds. 
    This function is typically used in scenarios where a timed response 
    is required, and it operates on a separate thread to allow concurrent 
    execution with other tasks.

    The function waits for 7 seconds, and if the first element of the 
    `answer` list is still `None` (indicating no user input), it assigns 
    the `default` value to `answer[0]`. After assigning the default value, 
    it simulates pressing the Enter key to proceed with the next step.

    Args:
        answer (list): A list that holds the user's response. The first 
                       element is updated with the default value if no 
                       response is received within the timeout period.
        default (bool): The boolean value to be assigned to `answer[0]` 
                        in case of a timeout.

    Raises:
        Exception: If an error occurs during execution, the exception is 
                   caught and a message is printed with details about 
                   the error.
    """
    try:
        time.sleep(7)
        if answer[0] == None:
            print(f"\nTimeout! Using default parameter")
            answer[0] = default
            # press Enter key
            keyboard_controller = Controller()
            keyboard_controller.press(Key.enter)
            keyboard_controller.release(Key.enter)
    except Exception as e:
        print(f"An error has occured(func: set_timer): {str(e)}")


def question_timer(message: str = "Set custom parameters") -> bool:
    """Sets up a time sensitive question "Set custom parameters", expecting a
    True or False response from the user if form of 'y/N'(yes or No). Using a 
    thread to call the set_timer function to facilitate concurrent execution
    which is automatically ended if there's a response before the timer runs-
    down.

    Returns:
        bool: _description_

    Raises:
        Exception: If an error occurs during execution, the exception is 
                   caught and a message is printed with details about 
                   the error.
    """
    try:
        question = [
            inquirer.Confirm("setup", message=message)
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
    """Sets up the desired parameter structure, by calling multiple functions
    each dictionary value is appended within the parameter dictionary based on
    each specific settings.

    Handles menu flow for all available settings.
    Returns:
        dict: custom parameter based on settings

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        # each function dictionary holder
        func_dict = {
            "Geographic Location": geo_location,
            "Localization": localization,
            "Pagination": pagination,
            "Advanced Parameters": advanced_parameters,
            "Advanced Filters": advanced_filters,
            "SerpApi Parameters": serpapi_parameters,
            "Reset Default parameters": reset_default_parameters,
        }
        # parameters

        parameters = {
            "engine": "google_reverse_image",
            "image_url": None,
            "no-cache": True,
        }
        while True:
            question = [
                inquirer.List("settings",
                              message="Select Settings",
                              choices=["Geographic Location", "Localization", "Pagination", "Advanced Parameters", "Advanced Filters", "SerpApi Parameters",
                                       "Reset Default parameters", "Exit"]),
            ]
            answers = inquirer.prompt(question)

            if answers["settings"] == "Exit":
                set_custom_parameter_to_default_parameter(parameters)
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
    """Read default parameter values from default_parameter.json
    file stored within the data folder

    Returns:
        dict: default parameter

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    data = None
    with open("./data/default_parameter.json", "r", encoding="utf8") as file:
        data = json.load(file)
    print("In default")
    return data


# Catalogue of custom settings function

def geo_location() -> dict:
    """geo_location menu;
        settings:
            location
            uule

    Returns:
        dict: {location|uule : {value}}

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
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
    """Setup the locations setings using inquire for prompting
    and parsing it's response.
    Using rapidfuzz for string matching for a smooth interface.

    Returns:
        dict: {location: {value}}

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
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
            input_text["location"], locations)
        matches = [match[0] for match in matches]
        matches.append(None)
        question2 = [
            inquirer.List(
                'location', message="Select Location", choices=matches)
        ]

        selected_loc = inquirer.prompt(question2)
        if selected_loc["location"]:
            return selected_loc
    except Exception as e:
        print(f"An error has occured(func: loaction_geo_location): {str(e)}")
# Function to get the top 10 closest matches using rapidwuzzy


def get_top_matches(user_input, location_list, filter=None, top_n=10) -> tuple:
    """Generate top "top_n" most similar string matches

    Args:
        user_input (_type_): _description_
        location_list (_type_): _description_
        filter (_type_, optional): _description_. Defaults to None.
        top_n (int, optional): _description_. Defaults to 10.

    Returns:
        tuple: matches
    """
    try:
        if filter:
            matches = process.extract(
                user_input, location_list, limit=top_n, scorer=filter)
            return matches
        else:
            matches = process.extract(user_input, location_list, limit=top_n)
            return matches
    except Exception as e:
        print(f"An error has occured(func: get_top_matches): {str(e)}")


def localization() -> dict:
    """localization menu setup for localization prameters

    Returns:
        dict: "google_domain": option["domain"],
                "gl": dict["country_code"],
                "hl": dict["language_code"]

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
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
                return localization_language()
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
    """Domain setup handler function, automatically assign parameters to,
    country, domain and language.

    Returns:
        dict: "google_domain": option["domain"],
                "gl": dict["country_code"],
                "hl": dict["language_code"]

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
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
    except Exception as e:
        print(f"An error has occured(func: localization_domain): {str(e)}")
# auto set parameters for associated values


def set_parameter(option: dict) -> dict:
    """Based on selected domain, automatically assign parameters to,
    country, domain and language.

    Args:
        option (dict): _description_

    Returns:
        dict:  "google_domain": option["domain"],
                "gl": dict["country_code"],
                "hl": dict["language_code"]

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
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
    except Exception as e:
        print(f"An error has occured(func: set_parameter): {str(e)}")
# set country parameter


def localization_country() -> dict:
    """Gets the list of countries from google_country txt file,
    assign country parameter

    Returns:
        dict: "gl": dict["country_code"]

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        countries = []  # get country list from google_country.txt
        with open("./data/google_country.txt", "r",  encoding="utf-8") as file:
            countries = file.readlines()
        countries = [country.strip() for country in countries]
        # question
        question = [
            inquirer.Text(
                "country", message="Input country of choice or List(to see all countries available)")
        ]
        answer = inquirer.prompt(question)

        if answer["country"].lower() == "list":
            question1 = [
                inquirer.List(
                    "country", message="Select a country", choices=countries)
            ]
            answer1 = inquirer.prompt(question1)
            if answer1["country"]:
                return set_country_code(answer1)

        # compare answer to list
        matches = get_top_matches(answer["country"], countries)
        matches = [match[0] for match in matches]  # top 5 matches
        matches.append(None)  # append None option for exit

        question1a = [
            inquirer.List("country", message="pick country", choices=matches)
        ]
        answer1a = inquirer.prompt(question1a)

        if answer1a:
            return set_country_code(answer1a)
    except Exception as e:
        print(f"An error has occured(func: localization_country): {str(e)}")

# set country code for localization country fuction


def set_country_code(option: dict) -> dict:
    """Sets counry parameter, full country name to abbreviation

    Args:
        option (dict): full country name

    Returns:
        dict: "gl": dict["country_code"]

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        data = None
        with open("./data/google-domains.json", "r", encoding="utf8") as file:
            data = json.load(file)
        for dict in data:
            if option["country"] in dict.values():  # auto assign value
                para = {
                    "gl": dict["country_code"],
                }
                print(para)
                return para
    except Exception as e:
        print(f"An error has occured(func: country_code): {str(e)}")

# set lanaguage parameter


def localization_language() -> dict:
    """Read list of available languages from google_language txt
    and pass to user for their prefered choice.

    Returns:
        dict: {language: {value}}

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        # get languages list from google_languages.txt
        languages = []
        with open("./data/google_languages.txt", "r",  encoding="utf-8") as file:
            languages = file.readlines()
        languages = [language.strip() for language in languages]

        question = [
            inquirer.Text(
                "language", message="Input language or List (List all languages)")
        ]
        answer = inquirer.prompt(question)

        if answer["language"].lower() == "list":
            question1 = [
                inquirer.List(
                    'language', message="Select a language", choices=languages)
            ]
            answer1 = inquirer.prompt(question1)

            if answer1["language"]:
                return set_language_parameter(answer1)

        # compare answer to list
        matches = get_top_matches(answer["language"], languages)
        matches = [match[0] for match in matches]  # top 5 matches
        matches.append(None)  # append None option for exit

        question1a = [
            inquirer.List("language", message="Select Language",
                          choices=matches)
        ]
        answer1a = inquirer.prompt(question1a)

        if answer1a:
            return set_language_parameter(answer1a)

    except Exception as e:
        print(f"An error has occured(func: localization_language): {str(e)}")

# set language code for localization_language function


def set_language_parameter(option: dict) -> dict:
    """Set language abbreviation name based on full name.

    Args:
        option (dict): Based on full language name

    Returns:
        dict: {"hl": dict["language_code"]}

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        data = None
        with open("./data/google-languages.json", "r", encoding="utf8") as file:
            data = json.load(file)
        for dict in data:
            if option["language"] in dict.values():
                para = {
                    "hl": dict["language_code"],  # auto assign value
                }
                print(para)
                return para
    except Exception as e:
        print(f"An error has occured(func: set_language_parameters): {str(e)}")


# pagination menu function

def pagination() -> dict:
    """Setup pagination parameter

    Returns:
        dict: {pagination: {value}}

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.    """
    try:
        while True:
            question1 = [
                inquirer.List("setting", message="Select settings", choices=[
                              "Result Offset", "Number of Results", "Go back"])
            ]
            answer1 = inquirer.prompt(question1)

            if answer1["setting"] == "Result Offset":
                question = [
                    inquirer.Text("start", message="start")
                ]
                answer = inquirer.prompt(question)
                if answer["start"]:
                    return answer
            elif answer1["setting"] == "Number of Results":
                question1a = [
                    inquirer.Text("num", message="num")
                ]
                answer1a = inquirer.prompt(question1a)
                if answer1a["num"]:
                    return answer1a
            else:
                break

    except Exception as e:
        print(f"An error has occured(func: pagination): {str(e)}")


# advanced filter menu function

def advanced_filters() -> dict:
    """Setup advanced filter

    Returns:
        dict: {Adult Content Filtering|Advanced Search Parameters: {value}}

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        while True:
            question = [
                inquirer.List("settings", message="Select setting",
                              choices=["Adult Content Filtering", "Advanced Search Parameters", "Go back"])
            ]
            answer = inquirer.prompt(questions=question)

            if answer["settings"] == "Adult Content Filtering":
                question1 = [
                    inquirer.List("safe", message="Select",
                                  choices=["active", "off", None])
                ]
                answer1 = inquirer.prompt(question1)
                if answer1["safe"]:
                    return answer1
            elif answer["settings"] == "Advanced Search Parameters":
                question2 = [
                    inquirer.Text("tbs", message="Enter tbs")
                ]
                answer2 = inquirer.prompt(question2)
                if answer2["tbs"]:
                    return answer2
            else:
                break
    except Exception as e:
        print(f"An error has occured(func: advanced_filters): {str(e)}")

# advanced_parameter settings


def advanced_parameters() -> dict:
    """Setup advance parameter setup

    Returns:
        dict: {image_url: {value}}

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        while True:
            question = [
                inquirer.Text("image_url", message="Image Url")
            ]
            answer = inquirer.prompt(question)
            if answer["image_url"]:
                return answer
            else:
                break
    except Exception as e:
        print(f"An error has occured(func: advanced_parameters): {str(e)}")


# serpapi_parameters settings

def serpapi_parameters() -> dict:
    """Setup serpapi parameter setting

    Returns:
        dict: {device|no_cache: {value}}

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        while True:
            question = [
                inquirer.List("settings", message="Select setting",
                              choices=["device", "no_cache", "engine", "async", "zero_trace", "Go back"])
            ]
            answer = inquirer.prompt(question)
            if answer["settings"] == "device":
                question1 = [
                    inquirer.List("device", message="Select device", choices=[
                                  "desktop", "tablet", "mobile"])
                ]
                answer1 = inquirer.prompt(question1)
                if answer1["device"]:
                    return answer1
            elif answer["settings"] == "no_cache":
                question1a = [
                    inquirer.List("no_cache", message="Disable Caching", choices=[
                                  "true", "false"], default="true")
                ]
                answer1a = inquirer.prompt(question1a)
                if answer1a["no_cache"] == "true":
                    return answer1a
            elif answer["settings"] == "engine":
                question1b = [
                    inquirer.Text("engine", message="Input search engine")
                ]
                answer1b = inquirer.prompt(question1b)
                if answer1b["engine"]:
                    return answer1b
            elif answer["settings"] == "zero_trace":
                question1c = [
                    inquirer.Confirm(
                        "zero_trace", message="Info: Enterprise Only. Do you want to turn ON zero_trace ?")
                ]
                answer1c = inquirer.prompt(question1c)

                if answer1c["zero_trace"]:
                    return answer1c
            elif answer["settings"] == "async":
                question1d = [
                    inquirer.Confirm("async", message="Turn on async")
                ]
                answer1d = inquirer.prompt(question1d)

                if answer1d["async"]:
                    return answer1d
            else:
                break
    except Exception as e:
        print(f"An error has occured(func: serpapi_parameters): {str(e)}")


# set custom parameter to default parameter

def set_custom_parameter_to_default_parameter(parameter_dict: dict) -> None:
    """A function hanlder for the custom_to_default function

    Args:
        parameter_dict (dict): custom parameter to be set to default 

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        while True:
            question = [
                inquirer.Confirm(
                    "set", message="Do you want to set custom settings as default settings ?")
            ]
            answer = inquirer.prompt(question)
            if answer["set"]:
                custom_to_default(parameter_dict)
                break
            else:
                break
    except Exception as e:
        print(f"An error has occured(func: set_custom_parameter_to_default_parameter): {
              str(e)}")

# custom to default function


def custom_to_default(parameter_dict: dict) -> None:
    """Sets custom parameter to default parameter

    Args:
        parameter_dict (dict): custom parameter to be set to default 

    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        json_object = json.dumps(parameter_dict, indent=4)
        with open("./data/default_parameter.json", "w", encoding="utf8") as file:
            file.write(json_object)
            print("Set to default settiings")
    except Exception as e:
        print(f"An error has occured(func: custom_to_default): {str(e)}")

# reset to default parameter


def reset_default_parameters() -> None:
    """reset default parameters; 
    to be used when custom parameter has been set to default


    Raises:
        Exception: If an error occurs during execution, the exception is 
                    caught and a message is printed with details about 
                    the error.
    """
    try:
        parameters = {
            "engine": "google_reverse_image",
            "image_url": None,
        }
        json_object = json.dumps(parameters, indent=4)
        with open("./data/default_parameter.json", "w", encoding="utf8") as file:
            file.write(json_object)
            print("Set to default settiings")
    except Exception as e:
        print(
            f"An error has occured(func: reset_default_parameters): {str(e)}")


# do something with the image name
def serp_search(params: dict, image_path: str, image_url: str) -> dict:
    try:
        # get api from .env
        env_path = find_dotenv()
        # load env to memory
        if not load_dotenv(env_path):
            raise EnvironmentError(
                "No .env file found or failed to load environment variables.")

        # update api & image url
        api = {
            "api_key": getenv("SERPAPI_KEY"),
            "image_url": image_url,
        }
        params.update(api)

        search = GoogleSearch(params)
        results = search.get_dict()
        if results:
            search_metadata = results.get("search_metadata", {})
            image_results = results.get("image_results", [])
            image_results_link = [links.get("link", "")
                                  for links in image_results]
            return {image_path: {"search_metadata_id": search_metadata.get("id", ""),
                                 "image_results": image_results_link
                                 }
                    }
        else:
            print(f"No search results found for {image_path}")
            return {}
    except Exception as e:
        print(
            f"An error has occured(func: serp_search): {str(e)}")
        return {}


if __name__ == "__main__":
    choice = question_timer()
    pprint(choice)
    if choice:
        parameters = custom_parameters()
    else:
        parameters = default_parameters()
    pprint(parameters)
    # result_json = serp_search(parameters)
