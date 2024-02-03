import numpy as np

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
