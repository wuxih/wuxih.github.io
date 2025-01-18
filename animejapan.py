import os
import requests
import json
from PIL import Image

JSON_URLS = [
    "https://prd.anime-japan.jp/exhibition_entry/storage/json/stage_red_ja.json",
    "https://prd.anime-japan.jp/exhibition_entry/storage/json/stage_blue_ja.json",
    "https://prd.anime-japan.jp/exhibition_entry/storage/json/stage_green_ja.json",
    "https://prd.anime-japan.jp/exhibition_entry/storage/json/stage_white_ja.json",
]

DOWNLOAD_FOLDER = "downloaded_images"

def download_images():
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    for url in JSON_URLS:
        response = requests.get(url)
        data = response.json()

        for item in data['response']['Date1']:
            image_url = item['image']
            if "_resize" in image_url:
                image_url = image_url.replace("_resize", "")

            image_name = os.path.basename(image_url)
            image_path = os.path.join(DOWNLOAD_FOLDER, image_name)

            if not os.path.exists(image_path):
                img_data = requests.get(image_url).content
                with open(image_path, 'wb') as handler:
                    handler.write(img_data)
                print(f"Downloaded: {image_path}")

def generate_metadata():
    images_metadata = []
    for image_name in os.listdir(DOWNLOAD_FOLDER):
        image_path = os.path.join(DOWNLOAD_FOLDER, image_name)
        if os.path.isfile(image_path):
            image_size = os.path.getsize(image_path)
            images_metadata.append({
                'name': image_name,
                'size': image_size,
            })

    with open('image_metadata.json', 'w') as f:
        json.dump(images_metadata, f, indent=4)

if __name__ == "__main__":
    download_images()
    generate_metadata()
