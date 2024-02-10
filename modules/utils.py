import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle

# get the path of the father of the current folder
CURRENT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

# handle price
def clean_price(df):
    # handle the price => removing the $ and remove empy spaces and make it float
    df['Price'] = df['Price'].str.replace(' ', '')
    df['Price'] = df['Price'].str.replace(',', '')
    df['Price'] = df['Price'].str.replace('$', '')
    df['Price'] = df['Price'].astype(float)
    
    # handle the outliers
    # we will use the IQT method
    # get the first and third quartile
    q1 = df['Price'].quantile(0.25)
    q3 = df['Price'].quantile(0.75)
    iqt = q3 - q1
    # remove the outliers
    df = df[(df['Price'] >= q1 - 1.5*iqt) & (df['Price'] <= q3 + 1.5*iqt)]

    # normalize the price
    df['Price'] = (df['Price'] - df['Price'].min()) / (df['Price'].max() - df['Price'].min())
    
    return df

# handle Age at time of purchase -> make it int
def clean_age(df):
    # if the case of df['Age at time of purchase'] is empty we make nan int
    # and then we fill the nan with the mean of the column
    df['Age at time of purchase'] = df['Age at time of purchase'].replace(' ', np.nan)
    df['Age at time of purchase'] = df['Age at time of purchase'].astype(float)
    return df

def handle_categorical_data(column):
    if column.dtype == "object":
        return column.astype('category').cat.codes
    
    return column

def handle_missing_values(column):
    # most repetitive value for categorical columns
    if column.dtype == "object":
        return column.fillna(column.mode()[0])
    # mean value for numerical columns
    else:
        return column.fillna(column.mean())
    
def clean_data(df):
    # handle Age at time of purchase
    df = clean_age(df)

    # handle the price => make the column float and handler the outliers of this columns
    # it is clear that price column is the only column that may have outliers
    df = clean_price(df)
    df = df.apply(handle_missing_values, axis=0)

    # remove unecessary columns
    # the columns whom contains 1 value only and the columns whom contain id in their name and we use capitalize
    df = df.drop(columns=df.columns[df.nunique() == 1])
    df = df.drop(columns=df.columns[df.columns.str.contains('id', case=False)])

    df = df.apply(handle_categorical_data, axis=0)

    # drop duplicated lines
    df = df.drop_duplicates()

    return df


def split_data(df):
    target = 'Mortgage'
    X = df.drop(target, axis=1)
    y = df[target]
    # Splitting the data into training and testing sets
    return train_test_split(X, y, test_size=0.3, random_state=123)

def get_split_data():
    X_train = pd.read_csv(f"{CURRENT_FOLDER}\\data\\X_train.csv")
    X_test = pd.read_csv(f"{CURRENT_FOLDER}\\data\\X_test.csv")
    y_train = pd.read_csv(f"{CURRENT_FOLDER}\\data\\y_train.csv")
    y_test = pd.read_csv(f"{CURRENT_FOLDER}\\data\\y_test.csv")
    return X_train, X_test, y_train, y_test

def get_models(model):
    if model == 'Logistic Regression':
        return pickle.load(open(f"{CURRENT_FOLDER}\\saved_models\\LogisticRegression.pkl",'rb'))
    elif model == 'Random Forest':
        return pickle.load(open(f"{CURRENT_FOLDER}\\saved_models\\RandomForestClassifier.pkl",'rb'))

def get_metrics(model):
    _, X_test, _, y_test = get_split_data()
    model = get_models(model)
    y_pred = model.predict(X_test)

    # return metrics as a df
    accuracy = metrics.accuracy_score(y_test, y_pred)
    precision = metrics.precision_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred)
    f1 = metrics.f1_score(y_test, y_pred)
    return pd.DataFrame({'Accuracy': [accuracy], 'Precision': [precision], 'Recall': [recall], 'F1': [f1]})

def get_roc_curve(model):
    _, X_test, _, y_test = get_split_data()
    model = get_models(model)
    # return the roc curve as a figure
    y_pred_proba = model.predict_proba(X_test)[:,1]
    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred_proba)
    return fpr, tpr, thresholds, metrics.roc_auc_score(y_test, y_pred_proba)


def get_confusion_matrix(model):
    _, X_test, _, y_test = get_split_data()
    model = get_models(model)
    # return the confusion matrix as a figure
    y_pred = model.predict(X_test)
    cm = metrics.confusion_matrix(y_test, y_pred)
    return cm