from pydantic import BaseModel


class ErrorMsg(BaseModel):
    Error: str
