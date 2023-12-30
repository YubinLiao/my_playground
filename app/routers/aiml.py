import urllib.request
import cv2
import numpy as np
from fastapi import (
    FastAPI,
    Response,
    HTTPException,
    APIRouter,
    Depends,
    BackgroundTasks,
    status,
)
from typing import Union
from .. import apimodels
from ..ml_models.traffic_sign import tsc

router = APIRouter(prefix="/aiml/v1.0", tags=["Machine Learning Services"])

tscmodel = tsc.tsc()


@router.post("/tsc", status_code=status.HTTP_200_OK)
async def traffic_sign_classification(imgurl: apimodels.traffic_sign):
    """
    input a traffic sign image url, return the classification of the image\n
    Note: model was trained with GTSRB deatset, the input image should be similar to\n
    the dataset for higher accuracy.
    :param imgurl: image url that contain image format shape in (w, h, 3)\n
    :return: classification of the traffic sign
    """
    try:
        req = urllib.request.urlopen(imgurl.image_url)
        img_array = np.array(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    img = cv2.resize(img, (30, 30), interpolation=cv2.INTER_AREA)
    images = []
    images.append(img)
    result, confidence = tscmodel.classify(images)
    if confidence > 0.9:
        return {"classification": result, "confidence": "{:.0%}".format(confidence)}
    else:
        return {"Message": "confidence too low, can't classify the image"}
