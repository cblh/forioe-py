# coding:utf-8
#!/usr/bin/python

import smtplib
import torndb
import datetime

def is_expired(last_request, last_report, end_time):
    today = datetime.datetime(int(str(datetime.date.today()).split('-')[0]),int(str(datetime.date.today()).split('-')[1]),int(str(datetime.date.today()).split('-')[2]))
    request = datetime.datetime(int(str(last_request).split('-')[0]),int(str(last_request).split('-')[1]),int(str(last_request).split('-')[2]))
    report = datetime.datetime(int(str(last_report).split('-')[0]),int(str(last_report).split('-')[1]),int(str(last_report).split('-')[2]))
    end = datetime.datetime(int(str(end_time).split('-')[0]),int(str(end_time).split('-')[1]),int(str(end_time).split('-')[2]))
    if (today - end).days > 0:
        return False
    elif (today - request).days > 0:
        return True
    elif (report - request).days > 0:
        return True
    else:
        return False

def sqlsearch():
    db = torndb.Connection('localhost', 'forioe', 'root', 'ybbiuggnav')
    sql = 'select * from `user`'
    result = db.query(sql)
    warnlist = {}
    for user in result:
        if user['last_request'] or user['last_report']:
            if is_expired(user['last_request'], user['last_report'], user['end_time']):
                warnlist[user['name']] = user['email']
    return warnlist

    
def sendmail(name, receivers):
    sender = 'forioe@guorunmin.cn'

    message = """From: forioe@guorunmin.cn
To: %s
Subject: 来自进度管理系统的提醒邮件

亲爱的%s
你收到这封邮件是因为系统检测到你还有报告未及时提交.
请尽快登录系统完成报告
""" % (receivers, name)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)   
        print "Successfully sent email"
    except:
        print "Error: unable to send email"
        print name, receivers

if __name__ == '__main__':
    data = sqlsearch();
    for user in data:
        print sendmail(str(user), str(data[user]))
        print user, data[user]
