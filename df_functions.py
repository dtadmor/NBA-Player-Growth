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


def use_history(df, player_id, year_col, columns, weight_col, span=2):

    # Creating a data frame to hold all of the weighted averages
    weighted_df = pd.DataFrame(index=df.index, columns=columns)

    # Create alpha using same method as ewm
    alpha = 2 / (span + 1)

    counter=0

    # Looping over the players
    for value in df[player_id].unique():

        # Saving the index of that filter
        index = df[df[player_id]==value].index

        # Saving the seasons that player played
        seasons = sorted(df.loc[index, year_col].unique(), reverse=True)

        # Looping over possible current seasons
        for i, current_season in enumerate(seasons):

            # Saving the information for the current season
            current_index = df.loc[index][df.loc[index, year_col]==current_season].index[0]
            current_weight = df.loc[current_index, weight_col]
            current_span = min(span, len(seasons)-i)

            # Creating the denominator for calculating the weighted average
            denominator = 1 * current_weight


            # Saving the weighted stats as the current season stats times the weight
            weighted_stats = df.loc[current_index, columns] * current_weight

            # Looping over past seasons according to the current span
            for n in range(1, current_span):

                # Saving the information for the past season
                past_season =  seasons[i+n]
                past_index = df.loc[index][df.loc[index, year_col]==past_season].index[0]
                past_weight = df.loc[past_index, weight_col]
                past_stats = df.loc[past_index, columns]

                # Updating the weighted stat and denominator
                weighted_stats += past_stats * past_weight * (alpha**n)
                denominator += past_weight * (alpha**n)

            # Saving their weighted values
            weighted_df.loc[current_index, columns] = weighted_stats / denominator

    # Renaming the columns
    weighted_df.rename(columns={col: col + '_WEIGHTED' for col in columns}, inplace=True)

    return weighted_df


# Function for mapping points from a category (assists, TO, etc.) to individual players
def pts_generated(series, values, play, category):

    # Calculating the points from the category using the value of that category in that season
    season = series['SEASON']
    points = values[season] * series[play + '_' + category]

    return points

# Function to merge a bunch of dataframes together
def merge_df(df_dict, columns_dict, how, on):

    # Initiating to show we need a master df
    have_master = False

    # Looping over dataframes
    for key, df in df_dict.items():

        # Getting the columns for the dataframe
        columns = columns_dict[key]

        # Merging the dataframes
        if have_master == False:
            master_df = df.loc[:, columns]
            have_master = True
        else:
            master_df = pd.merge(master_df, df[columns], how=how, on=on)

    return master_df


# Function to change the column names based on a prefix and condition
def update_columns(df, columns, prefix, condition):

    # Creating the new columns
    new_columns = [prefix + column if condition in column else column for column in columns]

    # Updating the columns for the dataframe
    df.columns = new_columns

    return df
