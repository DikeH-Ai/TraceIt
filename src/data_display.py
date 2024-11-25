import inquirer
from img_hash import archive_processor
from pprint import pprint


def display(imagepathList: list):
    try:
        while True:
            imagepathList.append("Exit")
            question = [
                inquirer.List("imagepath", message="Select an image",
                              choices=imagepathList)
            ]

            answer = inquirer.prompt(questions=question)
            path = answer["imagepath"]
            if path != "Exit":
                response = archive_processor(path)
            else:
                break
            while True:
                question1 = [
                    inquirer.List("data", message="Select data to be viewed",
                                  choices=["General", "New", "Go back"])
                ]

                answer1 = inquirer.prompt(questions=question1)

                if answer1["data"] == "General":
                    pprint(response["new"] + response["old"])
                elif answer1["data"] == "New":
                    pprint(response["new"])
                else:
                    break
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    display()
