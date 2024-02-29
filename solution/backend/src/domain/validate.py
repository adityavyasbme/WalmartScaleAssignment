
from pandas import DataFrame
from src.domain.models.definitions import calendar, sell_prices, sales
from src.domain.models.pydantic.tableDefinition import TableDefinition


def validate_expected_columns(df: DataFrame,
                              table_definition: TableDefinition) -> bool:
    """
    Validates that a DataFrame contains all expected columns as defined 
    in a TableDefinition.

    Args:
        df (DataFrame): The DataFrame to validate.
        table_definition (TableDefinition): The definition of the table, 
        including expected column names.

    Raises:
        Exception: If any expected columns are missing from the DataFrame.

    Returns:
        bool: True if the DataFrame contains all expected columns, otherwise 
        raises an Exception.
    """
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


def validate(raw_calendar_df: DataFrame,
             raw_sales_df: DataFrame,
             raw_sell_prices_df: DataFrame) -> None:
    """
    Validates that the provided DataFrames for calendar, sales, and 
    sell prices contain all the expected columns
    as defined in their respective TableDefinition.

    Args:
        raw_calendar_df (DataFrame): The DataFrame containing calendar data 
        to validate.
        raw_sales_df (DataFrame): The DataFrame containing sales data 
        to validate.
        raw_sell_prices_df (DataFrame): The DataFrame containing sell prices 
        data to validate.
    """
    validate_expected_columns(raw_calendar_df, calendar)
    validate_expected_columns(raw_sales_df, sales)
    validate_expected_columns(raw_sell_prices_df, sell_prices)
