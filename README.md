# TraceIt
TraceIt is an automated tool that performs reverse image searches using the Google Reverse Image API from SerpApi. It scans a designated folder of images and searches the web for any matches. It also sorts out new matches from the old one.
## Features
- Customizable Parameters: Set API parameters (like location) as needed for targeted searches.
- Organized Results: Displays search results with URLs.
- Track New Matches: Differentiates new matches from previous ones.

## Table of Contents

- [Project Overview](#project-overview)
- [Demo](#demo)
- [Requirements](#requirements)
- [Setup](#setup)
- [Modules](#modules)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

This project facilitates reverse image search and image comparison. It performs the following tasks:

1. Uploads images to Cloudinary for processing.
2. Performs reverse image search using SerpAPI.
3. Compares uploaded images using perceptual hashing to detect similarity.
4. Displays search results and compares them against historical data.

## Demo


## Requirements

- Python 3.x
- Required Python packages (requirements.txt)
- A Cloudinary account for image hosting and processing
- SerpAPI account for reverse image search

### Install Dependencies

Create a virtual environment and install the dependencies using the following command:

```bash
pip install -r requirements.txt
```

Where `requirements.txt` contains:

```plaintext
cloudinary
filetype
imagehash
inquirer
requests
python-dotenv
pillow
serpapi
```

## Setup

1. **Create an `.env` file** for storing sensitive credentials:
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
   - `SERPAPI_KEY`

2. **Image Directory**: Ensure the `./data/images/` directory exists with the images to be processed.

3. **History File**: The system expects a `./results/history.json` file for storing previous search results.

---

## Modules

### serp_function.py

This script interacts with SerpAPI to perform reverse image searches. It has two key functions:

- **`reset_default_parameters()`**: Resets the API parameters to their default values.
- **`serp_search()`**: Performs the reverse image search using parameters passed from the main function.

### img_processor.py

This module handles image processing tasks like checking if a file is an image and uploading images to Cloudinary.

- **`is_image()`**: Checks if a file is an image.
- **`image_processor()`**: Returns a list of valid image paths.
- **`upload_to_cloudinary()`**: Uploads images to Cloudinary and returns the URL and public ID.
- **`delete_image()`**: Deletes images from Cloudinary using the public ID.

### img_hash.py

This module is responsible for comparing images by generating perceptual hashes (pHash) to detect similar images.

- **`generate_phash()`**: Generates a perceptual hash for a given image.
- **`archive_processor()`**: Compares the current image's hash with archived images and returns new and old links based on similarity.

### data_display.py

This script handles the CLI for displaying results to the user. It uses the `inquirer` module for user interactions.

- **`display()`**: Displays a list of images for selection and allows the user to view "General" or "New" image links or go back.

---

## Usage

### Running the Project
First start by cloning repo:

```bash
git clone https://github.com/DikeH-Ai/TraceIt.git
```

Add images t the data/image folder

To run the project, execute the following command:

```bash
python .\\src\\setup.py
```

This will start the CLI for displaying image search results. You'll be prompted to select an image from the `./data/images/` directory and then choose to view the search results.

### Example Usage Flow

1. The script prompts you to select an image from the `./data/images/` folder.
2. Once an image is selected, the script fetches the image search results and compares them to previously archived data.
3. You can then choose to view "General" (all links), "New" (only new links), or go back to the image selection screen.

---

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. All contributions are welcome!

---

## License

This project is licensed under the MIT License.
