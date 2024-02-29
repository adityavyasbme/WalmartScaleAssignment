from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np


class MergeExogenousFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, calendar_df):
        self.calendar_df = calendar_df

    def fit(self, X, y=None):
        return self  # Nothing to fit

    def transform(self, X):
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


def get_cols(sales_df, n_forecast):
    train_df = sales_df.iloc[:, :-n_forecast].copy()
    valid_df = sales_df.iloc[:, -n_forecast:].copy()

    train_df_cols = [col for col in train_df.columns if col.startswith('d_')]
    fixed_cols = [col for col in train_df.columns if not col.startswith('d_')]
    valid_df_cols = [col for col in valid_df.columns if col.startswith('d_')]
    if not all([col in valid_df.columns for col in fixed_cols]):
        valid_df = pd.concat(
            [train_df[fixed_cols], valid_df], axis=1, sort=False)
    return (train_df_cols, fixed_cols, valid_df_cols, train_df, valid_df)


def get_sequences(data_array, input_slice_start_min, input_slice_start_max,
                  n_training, n_products_stores):

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
