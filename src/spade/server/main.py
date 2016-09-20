#!/usr/bin/env python3

import os
import sys
import redis

import spade.server.database as database
import spade.server.api

if __name__ == '__main__':
    r = redis.StrictRedis(host=os.environ['REDIS_PORT_6379_TCP_ADDR'], port=6379)
    r.flushall()

    db = database.Database(r)
    db.read()
    spade.server.api.listen(r)
