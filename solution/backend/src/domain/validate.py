
from src.domain.models.definitions import calendar, sell_prices, sales
from src.domain.models.pydantic.tableDefinition import TableDefinition


def validate_expected_columns(df, table_definition: TableDefinition):
    # Get expected column names from table definition
    expected_columns = table_definition.get_all_column_names()

    # Get actual column names from the DataFrame
    actual_columns = set(df.columns)

    # Check if all expected columns are present in the DataFrame
    missing_columns = set(expected_columns) - actual_columns
    if missing_columns:
        raise Exception(
            f"Invalid {table_definition.TableName} DataFrame." +
            f" Some expected columns are missing. Cols {missing_columns}")
    return True


def validate(raw_calendar_df, raw_sales_df, raw_sell_prices_df):
    validate_expected_columns(raw_calendar_df, calendar)
    validate_expected_columns(raw_sales_df, sales)
    validate_expected_columns(raw_sell_prices_df, sell_prices)
