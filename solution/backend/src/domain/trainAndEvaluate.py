from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, LSTM, BatchNormalization, Dense
from keras.metrics import RootMeanSquaredError
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, TensorBoard
import pandas as pd
import numpy as np
from pandas import DataFrame
from numpy import ndarray
from typing import Tuple
from sklearn.preprocessing import MinMaxScaler


def build_baseline_model(n_products_stores: int,
                         n_training: int,
                         n_outputs: int) -> Sequential:
    """
    Builds and compiles a baseline model with a CNN+LSTM architecture.

    Parameters:
    - n_products_stores (int): Number of products/stores features in the
    dataset.
    - n_training (int): Number of days used for training.
    - n_outputs (int): Number of output features (usually the same as
    n_products_stores).

    Returns:
    - Sequential: Compiled Keras model ready for training.
    """

    baseline_model = Sequential()

    conv1_filters = 64
    baseline_model.add(Conv1D(
        name='conv1', kernel_size=7, strides=1, padding="causal",
        activation="relu", filters=conv1_filters,
        input_shape=(n_training, n_products_stores)))
    baseline_model.add(MaxPooling1D(name='pool1'))

    baseline_model.add(Conv1D(
        name='conv2', kernel_size=7, strides=1, padding="causal",
        activation='relu',
        filters=int(baseline_model.get_layer('conv1').output.shape[2]/2)))
    baseline_model.add(MaxPooling1D(name='pool2'))

    lstm1_units = 256
    baseline_model.add(
        LSTM(name='lstm1', units=lstm1_units, return_sequences=True))
    baseline_model.add(BatchNormalization(name='norm1'))

    baseline_model.add(LSTM(
        name='lstm2',
        units=int(baseline_model.get_layer('lstm1').output.shape[2]/2),
        return_sequences=True))
    baseline_model.add(BatchNormalization(name='norm2'))

    baseline_model.add(LSTM(
        name='lstm3',
        units=int(baseline_model.get_layer('lstm2').output.shape[2]/2)))
    baseline_model.add(BatchNormalization(name='norm3'))

    baseline_model.add(Dense(name='dense', units=n_outputs))

    learning_rate = 0.001
    opt_adam = Adam(clipvalue=0.5, learning_rate=learning_rate)

    baseline_model.compile(loss='mse', optimizer=opt_adam,
                           metrics=[RootMeanSquaredError()])

    return baseline_model


def evaluate_model(model: Sequential,
                   X_valid: ndarray,
                   scaler: MinMaxScaler,
                   n_training: int,
                   n_outputs: int, valid_df_cols: list,
                   fixed_cols: list, valid_df_og: DataFrame) -> DataFrame:
    """
    Evaluates the model on the validation set and returns predictions as a 
    DataFrame.

    Parameters:
    - model (Sequential): Trained Keras model.
    - X_valid (ndarray): Validation input features.
    - scaler (MinMaxScaler): Scaler used for inverse transformation of 
    predictions.
    - n_training (int): Number of days used for training.
    - n_outputs (int): Number of output features.
    - valid_df_cols (list): List of column names for the validation DataFrame.
    - fixed_cols (list): List of fixed column names to be included in the 
    output DataFrame.
    - valid_df_og (DataFrame): Original validation DataFrame for merging 
    fixed columns.

    Returns:
    - DataFrame: Validation predictions merged with fixed columns.
    """

    y_valid_pred = []
    for X in X_valid:
        y_valid_pred_day = model.predict(X.reshape(1, n_training, n_outputs))
        y_valid_pred_day = scaler.inverse_transform(y_valid_pred_day)
        y_valid_pred.append(y_valid_pred_day)

    y_valid_pred_df = pd.DataFrame(
        np.array(
            [y_valid_pred[i].reshape(-1,) for i in range(
                len(y_valid_pred))]).T,
        columns=valid_df_cols)
    if not all([col in y_valid_pred_df.columns for col in fixed_cols]):
        y_valid_pred_df = pd.concat([valid_df_og[fixed_cols].reset_index(
            drop=True), y_valid_pred_df.reset_index(drop=True)], axis=1,
            sort=False)

    return y_valid_pred_df


def train_and_evaluate(
        n_outputs: int, X_train: ndarray,
        y_train: ndarray, X_valid: ndarray, y_valid: ndarray,
        epochs: int, batch_size: int,
        n_training: int, train_df_og: DataFrame,
        scaler: MinMaxScaler,
        valid_df_cols: list, fixed_cols: list,
        log_directory: str = "../results/baseline/tb_logs") -> Tuple[
            Sequential, DataFrame]:
    """
    Trains the baseline model and evaluates it on the validation set.

    Parameters:
    - n_outputs (int): Number of output features.
    - X_train (ndarray): Training input features.
    - y_train (ndarray): Training target features.
    - X_valid (ndarray): Validation input features.
    - y_valid (ndarray): Validation target features.
    - epochs (int): Number of epochs for training.
    - batch_size (int): Batch size for training.
    - n_training (int): Number of days used for training.
    - train_df_og (DataFrame): Original training DataFrame for 
    logging purposes.
    - scaler (MinMaxScaler): Scaler used for the inverse transformation 
    of predictions.
    - valid_df_cols (list): List of column names for the validation DataFrame.
    - fixed_cols (list): List of fixed column names to be included in the 
    output DataFrame.
    - log_directory (str): Directory for TensorBoard log files.

    Returns:
    - Tuple[Sequential, DataFrame]: Trained model and DataFrame containing
    validation predictions.
    """
    baseline_model = build_baseline_model(n_products_stores=n_outputs,
                                          n_training=n_training,
                                          n_outputs=n_outputs)
    baseline_model.summary()

    # Train baseline model with early stopping and tensorboard callbacks
    es = EarlyStopping(
        monitor='val_loss',
        mode='min',
        verbose=1,
        patience=20)

    _ = baseline_model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_valid, y_valid),
        callbacks=[es, TensorBoard(log_dir=log_directory)
                   ])

    # # Make predictions using baseline NN model
    baseline_model_pred_df = evaluate_model(
        baseline_model,
        X_valid,
        scaler,
        n_training,
        n_outputs,
        valid_df_cols,
        fixed_cols,
        train_df_og)
    return baseline_model, baseline_model_pred_df
