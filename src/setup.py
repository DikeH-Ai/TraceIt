import img_processor
import serp_fuction
from pprint import pprint
import json
from data_display import display
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='program.log',
                    encoding='utf-8', level=logging.DEBUG)


def main():
    try:
        # process the images in /data/image folder
        logging.info(">>>>Collecting images")
        print(">>>>Collecting images")
        imagepath = img_processor.image_processor()
        # upload processed images to cloud
        logging.info(">>>>Uploading images")
        print(">>>>Uploading images")
        image_dict = img_processor.upload_to_cloudinary(
            imagepaths=imagepath)  # image cloud url in dict

        # request for user response. Custom | Default parameters
        choice = serp_fuction.question_timer()
        logging.info(f">>>>Selected {choice}")
        print(f">>>>Selected {choice}")

        # function call based on choice
        if choice:
            parameters = serp_fuction.custom_parameters()
        else:
            parameters = serp_fuction.default_parameters()
        print(f">>>>Parameters set")

        result_dict = []

        # get data from data pool
        print(">>>>Gathering data")
        logging.info(">>>>Gathering data")
        for filepath, image_info in image_dict.items():
            # append function call dictionary to list
            url = image_info["url"]
            result_dict.append(serp_fuction.serp_search(
                # pass data to serp_search to get reverse images search data
                params=parameters, image_path=filepath, image_url=url))

        # save result to json file
        result_json = json.dumps(result_dict, indent=4)
        print(">>>>Saving data to json file")
        logging.info(">>>>Saving data to json file")

        with open("./results/reverse_image_search_results.json", "w", encoding="utf-8") as file:
            file.write(result_json)
        # get image path list
        image_path_list = []
        for entry in result_dict:
            for imagepath, values in entry.items():
                image_path_list.append(imagepath)

        print(">>>>Ready")
        logging.info(">>>>Ready")
        display(imagepathList=image_path_list)
        # request user response for 7s
        ques = "Would you like to delete images from cloud ?"
        delete_cloud_img = serp_fuction.question_timer(message=ques)

        if delete_cloud_img:
            img_processor.delete_image(image_dict=image_dict)

    except Exception as e:
        print(
            f"An unexpected error has occured (func: main(setup.py)): {str(e)}")


if __name__ == "__main__":
    main()
