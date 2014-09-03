from league.models import Player, League
import csv

def fill_league_with_players(league, player_file):
    with open(player_file, 'rb') as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            d = {}
            d['number'] = row['number']
            d['name'] = row['name']
            d['team'] = row['team']
            d['position'] = row['position'].lower()
            d['league'] = league
            league.player_set.create(**d)