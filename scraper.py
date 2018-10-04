import pandas as pd
import requests
import regex as re
import time
from bs4 import BeautifulSoup

# Creating a function to create a list of seasons to scrape
def past_seasons(n_years, end_year=18):

    # Create a list of years
    seasons = []
    for i in range(1, n_years + 1):
        start_year = 18 - i
        season = '20{}-{}'.format(start_year, end_year)
        seasons.append(season)
        end_year = start_year

    return seasons

# Creating a function to scrape the NBA wesbite
def nba_scraper(url, headers, n_years, verbose):

    # Initiate variables for the for loop
    df = pd.DataFrame()
    season_list = past_seasons(n_years)
    i = 1

    for season in season_list:

        # Creating the new url for the this season, scraping data, and saving it
        url = re.subf(r'Season=[-\d]+', 'Season={}'.format(season), url)
        result = requests.get(url, headers=headers)
        columns = result.json()['resultSets'][0]['headers']
        df = pd.concat([df, pd.DataFrame(result.json()['resultSets'][0]['rowSet'], columns=columns)], axis=0)

        # Updating the user and getting ready to scrape again
        if verbose > 0:
            print('Completed Scrape {} of {}'.format(i, len(season_list)))
        i += 1
        time.sleep(5)

    return df

# Creating a function to scrape for all of your URLs
def nba_multi_scraper(url_dict, headers, n_years, verbose=0):

    # Initialize the dictionary for the scraped data
    data_dict = {}

    for key, value in url_dict.items():
        # Add scraped data to the dictionary for each url
        data_dict[key] = nba_scraper(value, headers, n_years, verbose=verbose-1)
        if verbose > 0:
            print('Completed scrape of {}'.format(key))

    return data_dict

# Creating a function to scrape bball reference for total stats
def bball_reference_scraper(url, n_years, verbose):

    # Initiate variables for the for loop
    season_list = [str(year) for year in range(2018, 2018 - n_years, -1)]
    i = 1
    have_df = False

    for season in season_list:

        # Creating the new url for the this season and scraping data
        url = re.subf(r'NBA_[\d]+', 'NBA_{}'.format(season), url)
        result = requests.get(url)
        content = result.content.decode('utf-8')
        soup = BeautifulSoup(re.sub('<!--|-->', '', content), 'lxml')

        # Inputting the column names if they aren't there yet
        if have_df == False:
            columns = [item.text for item in soup.find('table', {'id': 'team_shooting'}).find('thead').find_all('tr')[2].find_all('th')]
            df = pd.DataFrame(columns=columns)
            have_df = True

        # Adding the shooting data to the dataframe
        shooting = ['']
        shooting.extend([item.text for item in soup.find('table', {'id': 'team_shooting'}).find('tfoot').find_all('td')])
        df.loc[season] = shooting

        # Updating the user and getting ready to scrape again
        if verbose > 0:
            print('Completed Scrape {} of {}'.format(i, len(season_list)))
        i += 1
        time.sleep(5)

    return df
