#!/usr/bin/env python3

import os
import sys

import spade.server.database as spade

if __name__ == '__main__':
    spade.process_sport(sys.argv[1])
