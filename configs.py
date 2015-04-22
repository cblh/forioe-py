# -*- coding:utf-8 -*-

import redis

http_port = '8888'

#db
mysql_master = 'localhost:3306'
mysql_slave = 'localhost:3306'
mysql_dbname = 'forioe'
mysql_user = 'root'
mysql_password = 'chenbaolin'

redis_host = 'localhost'
redis_port = 6379
redis_db = 0
cache_role_name = 'BLOG_USER_ROLE_'
cache_Connection = redis.StrictRedis(host=redis_host, port=redis_port, db=1)
