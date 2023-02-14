from sklearn.preprocessing import OneHotEncoder
import pandas as pd

def one_hot_encoding(data, target):
    '''
    One hot encodes dataframe
    '''

    # Split data into features (X) and labels (y)
    X = data.drop(target, axis=1)
    y = data[target]
    


    categorical_columns = [col for col in X.columns if X[col].dtype.name == "category"]

    encoder = OneHotEncoder()

    one_hot_encoded = pd.DataFrame(encoder.fit_transform(X[categorical_columns]).toarray(),
                                                         columns=encoder.get_feature_names_out(categorical_columns))

    # Drop original categorical columns and concatenate one-hot encoded columns
    X = X.drop(categorical_columns, axis=1)
 
    # Reset indexes to avoid row duplicates
    X = X.reset_index()
    one_hot_encoded = one_hot_encoded.reset_index()

    # Concatenate
    X = pd.concat([X, one_hot_encoded], axis=1)
    

    return(X, y)

