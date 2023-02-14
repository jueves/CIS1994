from sklearn.ensemble import RandomForestClassifier
from one_hot_encoding import one_hot_encoding
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

def RFC_train_and_evaluate(data, target, columns_to_drop, iterations=10):
    RFC_accuracy = []
    dummy_accuracy = []
    data = data.drop(columns_to_drop, axis=1)
    X, y = one_hot_encoding(data, target)
    for i in range(iterations):
        # Split the dataset into a training set and a test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        RFC = RandomForestClassifier(n_estimators=5, max_depth=4)
        RFC.fit(X_train, y_train)
        
        RFC_pred = RFC.predict(X_test)
        dummy_pred = dummy_model(y_train, X_test)

        RFC_accuracy.append(accuracy_score(y_test, RFC_pred))
        dummy_accuracy.append(accuracy_score(y_test, dummy_pred))

    print("RFC_Accuracy: {:.2f}%".format(np.mean(RFC_accuracy) * 100))
    print("Dummy_Accuracy: {:.2f}%".format(np.mean(dummy_accuracy) * 100))



def dummy_model(y_train, X_test):
    data = pd.Series(y_train)
    
    if isinstance(data.iloc[0], (int, float)):
        value = data.median
    else:
        value = data.mode()[0]
    
    prediction = [value]*len(X_test)
    
    return(prediction)

