from src.domain.configLoader import load_config_model


def transform_calendar(df):
    # TODO: Custom changes
    return df


def transform_sell_prices(df):
    # TODO: Custom changes
    return df


def transform_sales(df):
    # TODO: Custom changes
    return df


def transform(raw_calendar_df,
              raw_sales_df,
              raw_sell_prices_df):
    desired_model_level = load_config_model()
    if desired_model_level is None:
        raise ValueError(f"Model level {desired_model_level} not found.")

    calender_df = transform_calendar(raw_calendar_df)
    sales_df = transform_sales(raw_sales_df)
    sell_prices_df = transform_sales(raw_sell_prices_df)

    return calender_df, sales_df, sell_prices_df, desired_model_level


def get_model_details_per_level(sales_df, model_level):
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
