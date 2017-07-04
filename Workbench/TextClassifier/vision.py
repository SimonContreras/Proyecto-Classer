from google.cloud import vision, translate
import urllib.request
from os import remove
from entities import limpieza, juntar


def get_info_photo(url):
    # credentials and creation of service
    vision_client = vision.Client()
    translate_client = translate.Client()
    urllib.request.urlretrieve(url, "temp.jpg")

    # getting tags from a certain image and delete it
    image = vision_client.image(filename='temp.jpg')
    labels = image.detect_labels()
    remove('temp.jpg')

    # processing of tags and transform to string
    i = 0
    tags = []
    for label in range(len(labels)):
        try:
            translated_label = translate_client.translate(labels[i].description,
                                                          target_language='es',
                                                          format_='text',
                                                          source_language='en')
            tags.append(translated_label['translatedText'])
            i = i + 1
        except:
            tags.append(labels[i].description)
            i = i + 1

    return juntar(limpieza(tags))
