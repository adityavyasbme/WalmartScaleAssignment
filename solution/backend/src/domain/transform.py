from src.domain.configLoader import load_config_model


def transform_calendar(df):
    return df


def transform_sell_prices(df):
    return df


def transform_sales(df, model_level):

    return df


def transform(raw_calendar_df,
              raw_sales_df,
              raw_sell_prices_df,
              current_model_level):
    desired_model_level = load_config_model()
    if desired_model_level is None:
        raise ValueError(f"Model level {desired_model_level} not found.")

    calender_df = transform_calendar(raw_calendar_df)
    sales_df = transform_sales(raw_sales_df, model_level=desired_model_level)
    sell_prices_df = transform_sales(raw_sell_prices_df)

    return calender_df, sales_df, sell_prices_df
