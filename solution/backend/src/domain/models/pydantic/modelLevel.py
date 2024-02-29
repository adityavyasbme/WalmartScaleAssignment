from typing import List, Union
from pydantic import BaseModel


class ModelLevel(BaseModel):
    LevelId: int
    Description: str
    Columns: Union[str, List[str]]
