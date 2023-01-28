import os
from time import sleep

import requests
from bs4 import BeautifulSoup


def make_request(url):
    response = requests.get(url, allow_redirects=True).content
    soup = BeautifulSoup(response, "html.parser")

    return soup


def get_album_name_and_images(soup):
    images = [
        link.get("style")
        for link in soup.select("div.mdCMN09LiInner > span.mdCMN09Image")
    ]

    images = [
        i.lstrip('background-image: url("').rstrip(';compress=true");') for i in images
    ]

    album_name = soup.find("h3").get_text()

    file_format = images[0].split(".")[-1]

    return album_name, images, file_format


def download(album_name, images, file_format):
    try:
        os.mkdir(album_name)
    except FileExistsError:
        pass
    print("======", album_name, "======")

    for index, image in enumerate(images, 1):

        full_path = album_name + "/" + str(index).zfill(2) + "." + file_format

        r = requests.get(image)
        with open(full_path, "wb") as img_obj:
            img_obj.write(r.content)
            print(str(index))

    sleep(2)


def main(filename="urls.txt"):
    with open(filename, "r") as f:
        urls = [line.strip() for line in f]

    for i in urls:
        soup = make_request(i)
        album_name, images, file_format = get_album_name_and_images(soup)
        download(album_name, images, file_format)

        # break # debug


main()
