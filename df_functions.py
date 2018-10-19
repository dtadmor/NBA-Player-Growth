import pandas as pd

# Function to add the season to a data frame
def add_season(df):

    # If we already have season, return the data frame
    if 'SEASON' in df.columns:
        return df

    # Initialize variables up for the loop
    df = df.reset_index()
    season = 2019 # Since we immediately reduce it by 1

    # Loop through the data frame and add season
    for i in df.index:

        # When the "index" column hits 0, change to the next season
        if df.loc[i, 'index'] == 0:
            season -= 1

        # Save the season in the data frame
        df.loc[i, "SEASON"] = season

    # Turn the season in an int instead of a float
    df['SEASON'] = df['SEASON'].astype('int64')

    return df
