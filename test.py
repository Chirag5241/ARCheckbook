import os, io, sys
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd

def detectText(client, img):

    with io.open(img, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    df = pd.DataFrame(columns=['locale','description'])
    for text in texts:
        df = df.append(
                dict(
                    locale='en',
                    description=text.description
                    ),
                ignore_index=True
            )
    return df

def main():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceAccountToken.json'

    client = vision.ImageAnnotatorClient()

    output = detectText(client, "written_words.jpg")
    a = str(output['description'].array[0])
    return a.replace("\n", " ")
