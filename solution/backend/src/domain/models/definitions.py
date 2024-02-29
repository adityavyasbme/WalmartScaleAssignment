from src.domain.models.pydantic.modelLevel import ModelLevel
from src.domain.models.pydantic.tableDefinition import TableDefinition

# Define the data for the model levels
model_levels_data = [
    {"LevelId": 1,
     "Description": "Predict unit sales of all products," +
     "for all stores/states",
     "Columns": "for_all"},
    {"LevelId": 2,
     "Description": "Predict unit sales of all products, for each State",
     "Columns": "state_id"},
    {"LevelId": 3,
     "Description": "Predict unit sales of all products, for each store",
     "Columns": "store_id"},
    {"LevelId": 4,
     "Description": "Predict unit sales of all products, for each category",
        "Columns": "cat_id"},
    {"LevelId": 5,
     "Description": "Predict unit sales of all products, for each department",
        "Columns": "dept_id"},
    {"LevelId": 6,
     "Description": "Predict unit sales of all products, " +
     "for each State and category",
        "Columns": ["state_id", "cat_id"]},
    {"LevelId": 7,
     "Description": "Predict unit sales of all products, " +
     "for each State and department",
        "Columns": ["state_id", "dept_id"]},
    {"LevelId": 8,
     "Description": "Predict unit sales of all products, " +
     "for each store and category",
        "Columns": ["store_id", "cat_id"]},
    {"LevelId": 9,
     "Description": "Predict unit sales of all products, " +
     "for each store and department",
        "Columns": ["store_id", "dept_id"]},
    {"LevelId": 10,
     "Description": "Predict unit sales of product x, for all stores/states",
        "Columns": "item_id"},
    {"LevelId": 11,
     "Description": "Predict unit sales of product x, for each State",
        "Columns": ["item_id", "state_id"]},
    {"LevelId": 12,
     "Description": "Predict unit sales of product x, for each store",
        "Columns": ["item_id", "store_id"]}
]

table_definitions_data = [
    {
        "TableName": "calendar",
        "TableDescription": "Contains information " +
        " about the dates the products " +
        " are sold.",
        "Columns": [
            {"ColumnName": "date", "ColumnDescription": "The" +
             "  date in a 'y-m-d'" +
             "  format."},
            {"ColumnName": "wm_yr_wk",
                "ColumnDescription": "The id of the week the date" +
             "  belongs to."},
            {"ColumnName": "weekday",
                "ColumnDescription": "The type of the day (Saturday, " +
             " Sunday, ..., Friday)."},
            {"ColumnName": "wday",
                "ColumnDescription": "The id of the weekday, starting " +
             " from Saturday."},
            {"ColumnName": "month", "ColumnDescription": "The month of " +
             " the date."},
            {"ColumnName": "year", "ColumnDescription": "The year of the" +
             "  date."},
            {"ColumnName": "event_name_1",
                "ColumnDescription": "If the date " +
             " includes an event, the name" +
             "  of this event."},
            {"ColumnName": "event_type_1",
                "ColumnDescription": "If the date " +
             " includes an event, the type" +
             "  of this event."},
            {"ColumnName": "event_name_2", "ColumnDescription":
                "If the date includes a second event," +
             "  the name of this event."},
            {"ColumnName": "event_type_2", "ColumnDescription":
                "If the date includes a second event, the type of this event."}
        ]
    },
    {
        "TableName": "sell_prices",
        "TableDescription": "Contains information about the price of the " +
        " products sold per store and date.",
        "Columns": [
            {"ColumnName": "store_id",
                "ColumnDescription": "The id of the store where the product " +
             " is sold."},
            {"ColumnName": "item_id", "ColumnDescription": "The id of the" +
             "  product."},
            {"ColumnName": "wm_yr_wk", "ColumnDescription": "The id of the " +
             " week."},
            {"ColumnName": "sell_price", "ColumnDescription":
                "The price of the product for the given week/store. " +
             " The price" +
             "  is provided per week (average across seven days). " +
             " If not available, " +
             " this means that the product was not " +
             " sold during the examined week."}
        ]
    },
    {
        "TableName": "sales",
        "TableDescription": "Contains the historical daily" +
        "  unit sales data per" +
        "  product and store.",
        "Columns": [
            {"ColumnName": "item_id", "ColumnDescription": "The " +
             " id of the product."},
            {"ColumnName": "dept_id",
                "ColumnDescription": "The id of the department the " +
             " product belongs to."},
            {"ColumnName": "cat_id",
                "ColumnDescription": "The id of the category the " +
             " product belongs to."},
            {"ColumnName": "store_id",
                "ColumnDescription": "The id of the store where " +
             " the product is sold."},
            {"ColumnName": "state_id",
                "ColumnDescription": "The State where the store is located."},
            {"ColumnName": "d_1", "ColumnDescription":
                "The number of units sold at day 1, starting from " +
             " 2011-01-29."},
            # Add the remaining 'd_2' to 'd_1913' columns
            *[
                {"ColumnName": f"d_{i}", "ColumnDescription": "The" +
                 "  number of" +
                 f"  units sold at day {i}, starting " +
                 " from 2011-01-29."} for i in range(2, 1914)
            ]
        ]
    }
]


model_levels = [ModelLevel(**level_data) for level_data in model_levels_data]
[calendar, sell_prices, sales] = [TableDefinition(**table_data)
                                  for table_data in table_definitions_data]
