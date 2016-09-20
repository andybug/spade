#!/usr/bin/env python3

import os
import re
import csv
import json
import redis


class Database:
    def __init__(self, r):
        self.root = '/data'
        self.sports = []
        self.redis = r

    def read(self):
        sports = sorted(os.listdir(self.root))

        for sport in sports:
            path = os.path.join(self.root, sport)
            s = Sport(self, path, sport)
            s.read()
            self.sports.append(s)


class Sport:
    def __init__(self, db, root, sport):
        self.db = db
        self.root = root
        self.sport = sport
        self.seasons = []
        self.rounds = 0
        self.games = 0
        self.teams = 0
        self.teams_map = {}

    def read(self):
        print('reading sport %s from %s' % (self.sport, self.root))
        seasons = sorted(os.listdir(self.root))

        seasons_list = []

        for season in seasons:
            seasons_list.append(self.read_season(season))

        output = {}
        output['sport'] = self.sport
        output['seasons'] = seasons_list
        self.db.redis.set('%s:seasons' % self.sport, json.dumps(output, indent=2, sort_keys=True))

    def read_season(self, season):
        path = os.path.join(self.root, season)
        files = sorted(os.listdir(path))
        begin = self.rounds

        for f in files:
            matches = re.match(r'^round([0-9]{2})\.csv$', f)
            if matches != None:
                self.read_round(season, f)
                end = self.rounds
                self.rounds += 1

        print('season %s (%d - %d)' % (season, begin, end))
        output = {}
        output['season'] = int(season)
        output['first_round'] = begin
        output['last_round'] = end
        return output

    def read_round(self, season, round):
        path = os.path.join(self.root, season, round)
        begin = self.games

        games_list = []

        with open(path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                game = {}
                game['date'] = row[0]
                game['id'] = self.games
                game['hteam'] = row[2]
                game['hscore'] = int(row[3])
                game['ateam'] = row[4]
                game['ascore'] = int(row[5])
                game['neutral'] = bool(row[6])
                games_list.append(game)
                self.db.redis.rpush('%s:games' % self.sport, json.dumps(game, indent=2, sort_keys=True))
                end = self.games
                self.games += 1

        output = {}
        output['season'] = int(season)
        output['round'] = self.rounds
        output['games'] = games_list
        self.db.redis.rpush('%s:rounds' % self.sport, json.dumps(output, indent=2, sort_keys=True))

        print('round %d (%d - %d)' % (self.rounds, begin, end))
