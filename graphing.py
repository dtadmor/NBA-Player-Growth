import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to make scatter plots
def corr_plots(X, y, columns, cols=3):

    # Setting up the space for plotting
    n = len(columns)
    rows = (n + cols - 1)//cols
    plt.figure(figsize=(5*cols, 5*rows))
    plt.subplots_adjust(hspace=.3, wspace=.3)

    # Looping over the features and plotting them compared to the target
    for i, column in enumerate(columns):
        plt.subplot(rows, cols, i+1)
        plt.scatter(X[column], y)
        plt.xlabel(column)
        plt.ylabel(y.columns[0])

    return

# Function to create boxplots
def box_plots(X, y, columns, cols=3):

    # Setting up the space for plotting
    data = pd.concat([X, y], axis=1)
    n = len(columns)
    rows = (n + cols - 1)//cols
    plt.figure(figsize=(5*cols, 5*rows))
    plt.subplots_adjust(hspace=.3, wspace=.3)

    # Looping over the features and plotting them compared to the target
    for i, column in enumerate(columns):
        plt.subplot(rows, cols, i+1)
        sns.boxplot(x=column, y=y.columns[0], data=data)
        plt.xlabel(column)
        plt.ylabel(y.columns[0]);

    return

def graph_results(X_train, y_train, X_validate, y_validate, model,
                  axis_min=0, axis_max=1):
    # Plotting the predicted versus actual scores for the training and validation sets
    plt.scatter(model.predict(X_train), y_train, label='Train', alpha=.7)
    plt.scatter(model.predict(X_validate), y_validate, label='Validate', alpha=.7)
    plt.plot([axis_min, axis_max], [axis_min, axis_max], color='g', alpha=.5)
    plt.xlim([axis_min, axis_max])
    plt.ylim([axis_min, axis_max])
    plt.xlabel('Predicted Scores')
    plt.ylabel('Actual Scores')
    plt.legend();

    return
