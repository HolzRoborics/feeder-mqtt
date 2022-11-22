from typing import Optional

from pydantic import BaseModel


class TopicInit(BaseModel):
    Name: str
    WatchDog: Optional[int]

    Sender: Optional[str]
