from pydantic import BaseModel
from typing import List
from src.domain.models.pydantic.tableColumn import TableColumn


class TableDefinition(BaseModel):
    TableName: str
    Columns: List[TableColumn]

    def get_all_column_names(self) -> List[str]:
        return [column.ColumnName for column in self.Columns]
