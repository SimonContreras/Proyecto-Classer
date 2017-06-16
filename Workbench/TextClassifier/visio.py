from google.cloud import vision
from PIL import Image
import urllib.request

vision_client = vision.Client.from_service_account_json('client_key.json')

URL = 'http://www.w3schools.com/css/trolltunga.jpg'

with urllib.request.urlopen(URL) as url:
    with open('temp.jpg', 'rb') as f:
        bytes_image = vision_client.image(content=f.read())

labels = bytes_image.detect_labels()
print(labels.description)


