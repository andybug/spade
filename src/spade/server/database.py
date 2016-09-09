#!/usr/bin/env python3

import os
import re
import csv

def process_sport(path):
    seasons = sorted(os.listdir(path))

    for season in seasons:
        process_season(os.path.join(path, season))


def process_season(path):
    files = sorted(os.listdir(path))
    for f in files:
        matches = re.match(r'^round([0-9]{2})\.csv$', f)
        if matches != None:
            process_round(os.path.join(path, f), matches.group(1))


def process_round(path, rnd):
    rows = 0
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            rows = rows + 1

    print('%s: %d' % (rnd, rows))
    
