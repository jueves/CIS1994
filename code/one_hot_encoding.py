from sklearn.preprocessing import OneHotEncoder
import pandas as pd

def one_hot_encoding(data, target):
    '''
    One hot encodes dataframe
    '''
    categorical_columns = [col for col in data.columns if data[col].dtype.name == "category"]

    encoder = OneHotEncoder()

    one_hot_encoded = pd.DataFrame(encoder.fit_transform(data[categorical_columns]).toarray(),
                                                         columns=encoder.get_feature_names_out(categorical_columns))

    # Drop original categorical columns and concatenate one-hot encoded columns
    data = data.drop(categorical_columns, axis=1)
    data = pd.concat([data, one_hot_encoded], axis=1)

    # Split data into features (X) and labels (y)
    X = data.drop(target, axis=1)
    y = data[target]

    return(X, y)

