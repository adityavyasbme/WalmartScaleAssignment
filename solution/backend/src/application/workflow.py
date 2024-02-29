from src.infrastructure.dataLoader import load_csv_data
from src.domain import validate, transform


def get_raw_data():
    raw_calendar_df = load_csv_data('./data/calendar.csv')
    raw_sales_df = load_csv_data('./data/sales_train_validation.csv')
    raw_sell_prices_df = load_csv_data('./data/sell_prices.csv')
    return raw_calendar_df, raw_sales_df, raw_sell_prices_df


def pre_process(raw_calendar_df, raw_sales_df, raw_sell_prices_df):
    validate.validate(raw_calendar_df, raw_sales_df, raw_sell_prices_df)
    calender_df, sales_df, sell_prices_df = transform.transform(
        raw_calendar_df, raw_sales_df, raw_sell_prices_df)
    return calender_df, sales_df, sell_prices_df


def get_data():
    # Extract
    raw_calendar_df, raw_sales_df, raw_sell_prices_df = get_raw_data()
    # Transform
    calender_df, sales_df, sell_prices_df = transform(
        raw_calendar_df, raw_sales_df, raw_sell_prices_df)
    # Load
    # NOT DOING IT RN
    # Strategy 1 - We can save it, but keeping it dynamic for now
    # Strategy 2 - We can cache the function
    # Strategy 3 - Keeping everything abstract;
    #              If we chose PySpark we can take advantage of lazy loading
    return calender_df, sales_df, sell_prices_df


# def number_of_models():


# Step 1 - Get The Data
# data = load_csv_data()

# Step 2 - Do Exploration
# Not doing this because the data scientist has already done it
# PS - We can add this later if we want to make it interactive

# Step 3 - Pre Process
# Step 4 - Feature Engineering
# Step 5 - Feature Selection
# Step 6 - Split the data

# Step 7 - Define the Model

# Step 8 - Model Training
# Step 9 - Model Evaluation
# Step 10 - HyperParameter Tuning

# Step 11 - Model Selection & Logging

# Step 12 - Final Evaluation

# Step 13 - Deployment

# Step 14 - Monitoring and Maintenance
