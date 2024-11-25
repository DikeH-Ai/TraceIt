import img_processor
import serp_fuction
from pprint import pprint
import json
from data_display import display


def main():
    try:
        # process the images in /data/image folder
        imagepath = img_processor.image_processor()
        # upload processed images to cloud
        image_dict = img_processor.upload_to_cloudinary(
            imagepaths=imagepath)  # image cloud url in dict
        pprint(image_dict)
        # request for user response
        choice = serp_fuction.question_timer()
        pprint(choice)

        # function call based on choice
        if choice:
            parameters = serp_fuction.custom_parameters()
        else:
            parameters = serp_fuction.default_parameters()
        pprint(parameters)
        result_dict = []

        for filepath, image_info in image_dict.items():
            # append function call dictionary to list
            url = image_info["url"]
            result_dict.append(serp_fuction.serp_search(
                # pass data to serp_search to get reverse images search data
                params=parameters, image_path=filepath, image_url=url))

        # save result to json file
        result_json = json.dumps(result_dict, indent=4)

        with open("./results/reverse_image_search_results.json", "w", encoding="utf-8") as file:
            file.write(result_json)
        # get image path list
        image_path_list = []
        for entry in result_dict:
            for imagepath, values in entry.items():
                image_path_list.append(imagepath)
        display(imagepathList=image_path_list)
        # request user response for 7s
        ques = "Would you like to delete images from cloud ?"
        delete_cloud_img = serp_fuction.question_timer(message=ques)
        pprint(delete_cloud_img)

        if delete_cloud_img:
            img_processor.delete_image(image_dict=image_dict)

    except Exception as e:
        print(
            f"An unexpected error has occured (func: main(setup.py)): {str(e)}")


if __name__ == "__main__":
    main()
