from typing import Optional

from pydantic import BaseModel


class WatchdogData(BaseModel):
    Counter: int

    Sender: Optional[str]


class WatchdogInitResponse(BaseModel):
    Name: str
    WatchDog: int = 2

    Sender: Optional[str]
