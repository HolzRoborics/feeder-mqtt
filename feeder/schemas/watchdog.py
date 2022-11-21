from pydantic import BaseModel


class WatchdogData(BaseModel):
    Counter: int


class WatchdogInitResponse(BaseModel):
    Name: str
    WatchDog: str = 'OK'
