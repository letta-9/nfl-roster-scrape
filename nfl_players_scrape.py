from bs4 import BeautifulSoup as Soup
import requests
import pandas as pd
from pandas import DataFrame


teams = ['buffalo-bills', 'miami-dolphins', 'new-england-patriots', 'new-york-jets', 'baltimore-ravens', 'cincinnati-bengals', 
          'cleveland-browns', 'pittsburgh-steelers', 'houston-texans', 'indianapolis-colts', 'jacksonville-jaguars', 'tennessee-titans', 
              'denver-broncos', 'kansas-city-chiefs', 'las-vegas-raiders', 'los-angeles-chargers', 'dallas-cowboys', 'new-york-giants', 
                  'philadelphia-eagles', 'washington-commanders', 'chicago-bears', 'detroit-lions', 'green-bay-packers', 'minnesota-vikings', 
                      'atlanta-falcons', 'carolina-panthers', 'new-orleans-saints', 'tampa-bay-buccaneers', 'arizona-cardinals', 'los-angeles-rams',
                          'san-francisco-49ers', 'seattle-seahawks']

players = []
players_df = pd.DataFrame(players)

for x in teams:

    response = requests.get(f'https://www.nfl.com/teams/{x}/roster')
    soup = Soup(response.text, 'lxml')
    tables = soup.find_all('table')

    data = tables[0]
    rows = data.find_all('tr')

    def parse_row(row):
        return [str(x.string) for x in row.find_all('a')]

    list_of_parsed_rows = [parse_row(row) for row in rows]
    data_df = DataFrame(list_of_parsed_rows)

    players_df = pd.concat([players_df, data_df])


players_df = players_df.dropna()
players_df.rename(columns = {0:'name'}, inplace=True)
players_df = players_df['name'].str.lower()
players_df = players_df.str.replace('[^\w\s]','')
players_df = players_df.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

players_df.to_csv('nfl_list.csv', index=False)
