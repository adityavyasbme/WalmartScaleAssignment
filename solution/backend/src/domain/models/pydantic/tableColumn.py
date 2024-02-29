from pydantic import BaseModel


class TableColumn(BaseModel):
    ColumnName: str
    ColumnDescription: str
