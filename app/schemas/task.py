# app/schemas/task.py
from pydantic import BaseModel
from typing import Optional

class ImageTask(BaseModel):
    image_path: str
    user_id: Optional[int] = None