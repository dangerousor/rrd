#!/usr/bin/python
# -*- coding:utf-8 -*-
import redis

host = 'r-hp3ee2d77296a894.redis.huhehaote.rds.aliyuncs.com'
port = 6379
r = redis.StrictRedis(host=host, port=port)
