from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
from typing import Tuple, List
from pandas import DataFrame


class MergeExogenousFeatures(BaseEstimator, TransformerMixin):
    """
    A transformer that merges exogenous features from a calendar DataFrame
    into a sales DataFrame.
    """

    def __init__(self, calendar_df: DataFrame):
        """
        Initializes the transformer with the calendar dataframe.

        Args:
            calendar_df (DataFrame): The calendar DataFrame containing
            exogenous features.
        """
        self.calendar_df = calendar_df

    def fit(self, X: DataFrame, y: None = None) -> 'MergeExogenousFeatures':
        """
        Fit method for the transformer. Since this transformer does not learn
        from the data, it just returns itself.

        Args:
            X (DataFrame): The input data to transform.
            y (None, optional): Ignored. Defaults to None.

        Returns:
            MergeExogenousFeatures: The transformer itself.
        """
        return self

    def transform(self, X: DataFrame) -> DataFrame:
        """
        Transforms the sales data by merging it with exogenous features
        from the calendar data.

        Args:
            X (DataFrame): The sales data DataFrame to transform.

        Returns:
            DataFrame: The transformed sales DataFrame with exogenous
            features merged.
        """
        # Ensure the calendar_df has necessary flags
        self.calendar_df['event_1_flag'] = self.calendar_df[
            'event_name_1'].notna(
        ).astype(int)
        self.calendar_df['event_2_flag'] = self.calendar_df[
            'event_name_2'].notna(
        ).astype(int)
        # Transpose sales data
        sales_t_df = X[[col for col in X.columns if col not in [
            'id', 'item_id', 'dept_id',
            'cat_id', 'store_id', 'state_id']]
        ].T.reset_index().rename(columns={'index': 'd'})

        # Merge exogenous features from calendar_df
        sales_t_exo_df = pd.merge(sales_t_df, self.calendar_df[[
                                  'd', 'snap_CA', 'snap_TX', 'snap_WI',
                                  'event_1_flag', 'event_2_flag']], on='d',
                                  how='left').drop(columns=['d'])

        # Convert all column names to strings to satisfy MinMaxScaler
        # requirements
        sales_t_exo_df.columns = sales_t_exo_df.columns.astype(str)

        return sales_t_exo_df


def get_cols(
        sales_df: DataFrame,
        n_forecast: int) -> Tuple[
            List[str], List[str], List[str], DataFrame, DataFrame]:
    """
    Prepares column lists and splits the sales DataFrame into training
    and validation sets.

    Args:
        sales_df (DataFrame): The sales DataFrame to process.
        n_forecast (int): The number of days to forecast (used to split
        the data).

    Returns:
        Tuple[List[str], List[str], List[str], DataFrame, DataFrame]: Tuple
        containing lists of training columns,
        fixed columns, validation columns, and the training and validation
        DataFrames.
    """
    train_df = sales_df.iloc[:, :-n_forecast].copy()
    valid_df = sales_df.iloc[:, -n_forecast:].copy()

    train_df_cols = [col for col in train_df.columns if col.startswith('d_')]
    fixed_cols = [col for col in train_df.columns if not col.startswith('d_')]
    valid_df_cols = [col for col in valid_df.columns if col.startswith('d_')]
    if not all([col in valid_df.columns for col in fixed_cols]):
        valid_df = pd.concat(
            [train_df[fixed_cols], valid_df], axis=1, sort=False)
    return (train_df_cols, fixed_cols, valid_df_cols, train_df, valid_df)


def get_sequences(data_array: np.ndarray,
                  input_slice_start_min: int,
                  input_slice_start_max: int,
                  n_training: int,
                  n_products_stores: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates input and output sequences for training and validation.

    Args:
        data_array (np.ndarray): The data array to generate sequences from.
        input_slice_start_min (int): The starting index for generating
        sequences.
        input_slice_start_max (int): The ending index for generating sequences.
        n_training (int): Number of days used for training.
        n_products_stores (int): Number of product/store combinations.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Input (X) and output (y) sequences.
    """

    X = []
    y = []
    for i in range(input_slice_start_min, input_slice_start_max):
        # print a few slices at the start and end for debugging
        # if i<=input_slice_start_min+2 or i>input_slice_start_max-4:
        #     print('Input:',range(i,i+n_training),',  Output:',i+n_training)
        X.append(data_array[i:i+n_training])
        y.append(data_array[i+n_training, :n_products_stores])

    return X, y


def process(sales_df,
            calendar_df,
            n_training=28,
            n_forecast=28):
    (train_df_cols, fixed_cols,
     valid_df_cols, train_df_og,
     valid_df_og) = get_cols(sales_df, n_forecast)
    merge_exogenous_features = MergeExogenousFeatures(calendar_df=calendar_df)
    sales_df_exogenous = merge_exogenous_features.fit_transform(sales_df)
    train_df = sales_df_exogenous.iloc[:-n_forecast, :]
    valid_df = sales_df_exogenous.iloc[-n_forecast:, :]
    scaler = MinMaxScaler(feature_range=(0, 1))
    train_df.columns = train_df.columns.astype(str)
    valid_df.columns = valid_df.columns.astype(str)
    train_df = scaler.fit_transform(train_df)
    valid_df = scaler.transform(valid_df)

    n_products_stores = train_df[0].shape[0]

    X_train, y_train = get_sequences(train_df, 0,
                                     train_df.shape[0]-n_training,
                                     n_training,
                                     n_products_stores)
    train_valid_df = np.concatenate((train_df, valid_df), axis=0)

    X_valid,  y_valid = get_sequences(train_valid_df,
                                      train_valid_df.shape[0] -
                                      n_training-n_forecast,
                                      train_valid_df.shape[0]-n_forecast,
                                      n_training,
                                      n_products_stores)

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_valid = np.array(X_valid)
    y_valid = np.array(y_valid)
    return (X_train, y_train, X_valid, y_valid,
            n_products_stores,
            scaler,
            valid_df_cols,
            fixed_cols,
            train_df_og,
            valid_df_og,
            train_df,
            valid_df)
