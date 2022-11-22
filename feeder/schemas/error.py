from typing import Optional

from pydantic import BaseModel


class ErrorMsg(BaseModel):
    Error: str

    Sender: Optional[str]
