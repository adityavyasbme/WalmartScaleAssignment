from pandas import DataFrame
from typing import Tuple, Generator
from src.domain.configLoader import load_config_model
from src.domain.models.pydantic.modelLevel import ModelLevel


def transform_calendar(df: DataFrame) -> DataFrame:
    """
    Apply custom transformations to the calendar DataFrame.

    Args:
        df (DataFrame): The raw calendar DataFrame.

    Returns:
        DataFrame: The transformed calendar DataFrame.
    """
    # TODO: Custom changes
    return df


def transform_sell_prices(df: DataFrame) -> DataFrame:
    """
    Apply custom transformations to the sell prices DataFrame.

    Args:
        df (DataFrame): The sell prices DataFrame.

    Returns:
        DataFrame: The transformed sell prices DataFrame.
    """
    # TODO: Custom changes
    return df


def transform_sales(df: DataFrame) -> DataFrame:
    """
    Apply custom transformations to the sales DataFrame.

    Args:
        df (DataFrame): The raw sales DataFrame.

    Returns:
        DataFrame: The transformed sales DataFrame.
    """
    # TODO: Custom changes
    return df


def transform(raw_calendar_df: DataFrame,
              raw_sales_df: DataFrame,
              raw_sell_prices_df: DataFrame) -> Tuple[DataFrame, DataFrame,
                                                      DataFrame, ModelLevel]:
    """
    Transform raw dataframes according to the specified model level 
    configurations.

    Args:
        raw_calendar_df (DataFrame): Raw calendar data.
        raw_sales_df (DataFrame): Raw sales data.
        raw_sell_prices_df (DataFrame): Raw sell prices data.

    Raises:
        ValueError: If the desired model level configuration is not found.

    Returns:
        Tuple[DataFrame, DataFrame, DataFrame, ModelLevel]: Transformed 
        calendar, sales, and sell prices DataFrames,
        along with the desired model level.
    """
    desired_model_level = load_config_model()
    if desired_model_level is None:
        raise ValueError(f"Model level {desired_model_level} not found.")

    calender_df = transform_calendar(raw_calendar_df)
    sales_df = transform_sales(raw_sales_df)
    sell_prices_df = transform_sales(raw_sell_prices_df)

    return calender_df, sales_df, sell_prices_df, desired_model_level


def get_model_details_per_level(
        sales_df: DataFrame,
        model_level: ModelLevel) -> Tuple[DataFrame, Generator]:
    """
    Group sales data according to the specified model level and calculate the 
    count of time series for each group.

    Args:
        sales_df (DataFrame): The sales DataFrame.
        model_level (ModelLevel): The model level configuration.

    Returns:
        Tuple[DataFrame, Generator]: A DataFrame summarizing the count of time
        series for each model level group,
        and a generator for iterating through each group in the sales 
        DataFrame.
    """
    sales_df['for_all'] = "all"
    if isinstance(model_level.Columns, list):
        list_groupby = model_level.Columns
    else:
        list_groupby = [model_level.Columns]
    print(list_groupby)
    d1 = sales_df.groupby(list_groupby).count().reset_index()[
        list_groupby+['id']].rename(columns={
            'id': 'number of raw time series for' +
            ' training each model at level '+str(model_level.LevelId)})
    d2 = sales_df.groupby(list_groupby)
    return d1, d2
