import csv
import os
import numpy as np
from pathlib import Path
import tensorflow as tf
import urllib.request
import cv2


PATH = Path(__file__).parent.resolve()
MAPPING_FILE = os.path.join(PATH, "sign_mapping.csv")
MODEL_PATH = os.path.join(PATH, "model.keras")


class tsc:
    def __init__(self):
        # trafficsign.train_model()
        self.mapping = self.load_sign_mapping()
        self.model = tf.keras.models.load_model(MODEL_PATH)

    def load_sign_mapping(self):
        mapping = {}

        with open(MAPPING_FILE) as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                mapping[int(row[0])] = row[1]
        return mapping

    def classify(self, imgs):
        prediction = self.model.predict(np.array(imgs))[0]
        result = np.argmax(prediction)
        confidence = "{:.0%}".format(prediction[result])
        print(f"classification code{result}: confidence {confidence}")
        return (self.mapping[result], prediction[result])

    def classify_url(self, img_url: str):
        req = urllib.request.urlopen(img_url)
        img_array = np.array(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)
        img = cv2.resize(img, (30, 30), interpolation=cv2.INTER_AREA)
        images = []
        images.append(img)
        prediction = self.model.predict(np.array(images))[0]
        result = np.argmax(prediction)
        print(self.mapping[result])
        confidence = "{:.0%}".format(prediction[result])
        print(confidence)


if __name__ == "__main__":
    predic = tsc()
    predic.classify_url(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4csNyTJYlM8MZZn-bA2cEREMIjoGwW-V4iA&usqp=CAU"
    )
