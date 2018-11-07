import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from itertools import combinations

# Function to get future or past data for a player
def shift_data(df, on, columns, prefix='TARGET_', amount=1):

    # Create a copy of the df so as to not mess with the original df
    new_df = df.copy()

    # For each value, filter the df and shift the columns the specified amount
    for value in df[on].unique():
        index = df[df[on]==value].index

        for column in columns:
            new_df.loc[index, prefix+column] = df.loc[index, column].shift(amount)

    return new_df

def data_split(X, y, category, test_size=.2, validate_size=.2):

    # Dropping players that don't have a target
    drop_index = y[y['TARGET_' + category].isna()].index
    y.drop(drop_index, inplace=True)
    X.drop(drop_index, inplace=True)

    # Dropping the rows when the player has NANs for that category in the current season
    X = X[~X[category].isna()]
    index = X.index
    y = y.loc[index]

    # Determining what to set 'test_size' in the split for the validation set
    validate_size = validate_size/(1 - test_size)

    # Creating the train, validate, and test from X and y.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    X_train, X_validate, y_train, y_validate = train_test_split(X_train, y_train, test_size=validate_size, random_state=42)

    return X_train, X_validate, X_test, y_train, y_validate, y_test

# Function for finding feautres highly correlated with the target
def corr_finder(X, y, cutoff, size=None):

    # Finding the numeric columns
    numeric_columns = X.select_dtypes(['float', 'int']).columns

    # Creating a df of correlations (rows are predictive features, columns are target features)
    df = pd.concat([X,y], axis=1).corr().loc[numeric_columns, y.columns]

    # Creating a blank features list
#     corr_features = []

    feature = y.columns[0]

    # Saving the better correlated predictive features
    corr_features = list(df[abs(df[feature]) > cutoff].abs().sort_values(feature, ascending=False).index)

    # Making sure the number of correlated features is not greater than the 'size'
    if size:
        if len(corr_features) > size:
            corr_features = corr_features[:size]

    return corr_features

def feature_selection_corr(X, y, alpha=.4, beta=.7):

    numeric_columns = X.select_dtypes(['float', 'int']).columns

    possible_features = []
    for column in numeric_columns:
        coef = np.corrcoef(X[column], y)[0,1]
        if abs(coef) > alpha:
            possible_features.append([column, coef])

    possible_features.sort(key = lambda feature: feature[1], reverse=True)
    possible_features= [feature for feature, _ in possible_features]

    colinear_features = []
    for row, column in combinations(possible_features, 2):
        if np.corrcoef(X[row], X[column])[0,1] > beta:
            colinear_features.append([[row, np.corrcoef(X[row], y)[0,1]], [column, np.corrcoef(X[column], y)[0,1]]])

    suggested_features = possible_features
    for choice in colinear_features:
        if (choice[1][0] in suggested_features) and (choice[0][0] in suggested_features):
            if choice[0][1] >= choice[1][1]:
                suggested_features.remove(choice[1][0])
            else:
                suggested_features.remove(choice[0][0])

    return suggested_features
