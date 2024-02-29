import os
import json
import re
from typing import Tuple, Dict, Any, List
from pandas import DataFrame
from fastapi import APIRouter
from concurrent.futures import ProcessPoolExecutor, as_completed
from src.infrastructure.dataLoader import load_csv_data
from src.domain import (validate, transform, preProcessing,
                        trainAndEvaluate, configLoader)

router = APIRouter()


def get_data() -> Tuple[DataFrame, DataFrame, int]:
    """
    Load and preprocess data, then return transformed data frames and 
    desired model level.

    Returns:
    Tuple[DataFrame, DataFrame, int]: Calendar data frame, sales data frame, 
    and desired model level.
    """
    raw_calendar_df = load_csv_data('./data/calendar.csv')
    raw_sales_df = load_csv_data('./data/sales_train.csv').iloc[0:100]
    raw_sell_prices_df = load_csv_data('./data/sell_prices.csv')

    validate.validate(raw_calendar_df, raw_sales_df, raw_sell_prices_df)
    calender, sales, _, desired_model_level = transform.transform(
        raw_calendar_df, raw_sales_df, raw_sell_prices_df)
    return calender, sales, desired_model_level


def run_multiple_model() -> None:
    """
    Load configuration, get data, and execute model training in 
    parallel processes.
    """
    config_dict = configLoader.load_config()
    epochs = config_dict['epochs']
    calender_df, sales_df, desired_model_level = get_data()
    _, d2 = transform.get_model_details_per_level(
        sales_df, desired_model_level)

    # Using a ProcessPoolExecutor to run models in parallel
    with ProcessPoolExecutor(max_workers=os.cpu_count()-1) as executor:
        # Dictionary to hold futures
        futures = {}

        for group_name, group_df in d2:
            # Submitting the run_model function to the executor
            # Pass additional arguments as needed
            future = executor.submit(
                run_model, group_name, group_df, calender_df, epochs)
            futures[future] = group_name

        # As each future completes, get the result and populate temp_models
        for future in as_completed(futures):
            group_name = futures[future]
            try:
                future.result()
            except Exception as exc:
                print(f'Generated an exception: {exc}')


def run_model(group_name: str,
              sales_df: DataFrame,
              calendar_df: DataFrame,
              epochs: int) -> None:
    """
    Process data, train and evaluate model, and save results.

    Parameters:
    - group_name: The name of the group for which the model is being run.
    - sales_df: DataFrame containing sales data.
    - calendar_df: DataFrame containing calendar data.
    - epochs: Number of epochs to train the model.
    """
    print(f"Running {group_name}")
    try:
        sales_df.drop(columns=['for_all'], inplace=True)
    except Exception as e:
        print(e)
        pass
    (X_train, y_train, X_valid, y_valid,
     n_products_stores, scaler, valid_df_cols,
     fixed_cols, train_df_og,
     valid_df_og,
     train_df,
     valid_df) = preProcessing.process(sales_df,
                                       calendar_df,
                                       n_training=28,
                                       n_forecast=28)

    model, baseline_model_pred_df = trainAndEvaluate.train_and_evaluate(
        n_outputs=n_products_stores,
        X_train=X_train,
        y_train=y_train,
        X_valid=X_valid,
        y_valid=y_valid,
        epochs=epochs,
        batch_size=10,
        n_training=28,
        train_df_og=valid_df_og,
        scaler=scaler,
        valid_df_cols=valid_df_cols,
        fixed_cols=fixed_cols)

    # Construct a unique filename for each process's output
    filename = f"./results/{group_name}_results.json"
    print(type(train_df_og))
    print(type(valid_df_og))
    print(type(baseline_model_pred_df))

    data = {
        "valid_df": valid_df_og.to_dict(),
        'pred_df': baseline_model_pred_df.to_json(),
    }
    # Ensure the results directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # Write results to a JSON file
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"Results for {group_name} saved to {filename}")


@router.get("/api/modelNames")
def fetch_model_names() -> List[str]:
    """
    Fetch and return the names of all model groups from the results directory.

    Returns:
    List[str]: A list containing model group names.
    """
    # Directory where results JSON files are stored
    results_dir = './results'
    # List all files in the results directory
    files = os.listdir(results_dir)
    # Filter files to get only those ending with '_results.json'
    results_files = [file for file in files if file.endswith('_results.json')]
    group_names = [re.sub(r'_results\.json$', '', file)
                   for file in results_files]

    return group_names


@router.post("/api/modelData")
def fetch_model_store(key) -> Dict[Any, Any]:
    """
    Fetch and return model results for a specific key.

    Parameters:
    - key: Name of Group

    Returns:
    Dict[str, Any]: A dictionary containing model group names.
    """
    # Directory where results JSON files are stored
    results_dir = './results/'

    # Construct the filename based on the key
    filename = f"{key}_results.json"
    file_path = os.path.join(results_dir, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file doesn't exist, return a 404 error
        raise Exception("Model data not found")

    # Read and return the JSON data
    with open(file_path, 'r') as f:
        data = json.load(f)

    return data
