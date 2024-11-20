import img_processor
import serp_fuction
import pprint
import json


def main():
    try:
        # process the images in /data/image folder
        imagepath = img_processor.image_processor()
        # upload processed images to cloud
        image_dict = img_processor.upload_to_cloudinary(
            imagepaths=imagepath)  # image cloud url in dict

        # request for user response
        choice = serp_fuction.question_timer()
        pprint(choice)

        # function call based on choice
        if choice:
            parameters = serp_fuction.custom_parameters()
        else:
            parameters = serp_fuction.default_parameters()
        pprint(parameters)
        result_json = []
        for img in image_dict:
            # append function call dict to list
            result_json.append(serp_fuction.serp_search(
                # pass data to serp_search to get reverse images search data
                params=parameters, image_path=img.key(), image_url=img["url"]))

        # save result to json file
        result_json = json.dumps(result_json)

        with open("./results/reverse_image_search_results.json", "w", encoding="utf-8") as file:
            file.write(result_json)

        # request user response for 7s
        ques = "Would you like to delete images from cloud ?"
        delete_cloud_img = serp_fuction.question_timer(message=ques)
        pprint(delete_cloud_img)

        if delete_cloud_img:
            img_processor.delete_image(image_dict=image_dict)

        # remember function

    except Exception as e:
        print(
            f"An unexpected error has occured (func: main(setup.py)): {str(e)}")


if __name__ == "__main__":
    main()
