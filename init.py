# coding:utf-8
#!/usr/bin/env python
import torndb
import os
import time
def truncate():
    db = torndb.Connection('localhost', 'forioe', 'root', 'chenbaolin')
    sql1 = 'truncate table `user`; truncate table `report`; truncate table `response`'
    try:
    	db.query(sql1)
    	print 'truncate success'
    except Exception,e:
    	print 'truncate failed',e
    time.sleep(2)
    try:
    	os.system('mysql -uroot -pchenbaolin forioe < init.sql')
    except Exception,e:
    	print 'import failed',e


if __name__ == '__main__':
	truncate()
