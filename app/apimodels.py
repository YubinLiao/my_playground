from pydantic import BaseModel
from typing import Optional


class JobIn(BaseModel):
    script_path: str = "robot/TestCases"
    tag: Optional[str] = "uiORapi"
    headless: Optional[bool] = True
    browser: Optional[str] = "chromium"
    recordVideo: Optional[bool] = False


class traffic_sign(BaseModel):
    image_url: str
