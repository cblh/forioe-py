# -*- coding:utf-8 -*-
import models.db
import datetime
import lib.pxfilter as pxfilter
import time
import smtplib
class Process(object):

    # def __init__(self):
    #     self.M = models.db.base()
    #     self.M.db_name = 'process'
    #     self.stuid = studentid


    def process(self, start_time, end_time):
        
        start_time =datetime.datetime(int(str(start_time).split('-')[0]),int(str(start_time).split('-')[1]),int(str(start_time).split('-')[2]))
        end_time =datetime.datetime(int(str(end_time).split('-')[0]),int(str(end_time).split('-')[1]),int(str(end_time).split('-')[2]))
        today = datetime.datetime(int(str(datetime.date.today()).split('-')[0]),int(str(datetime.date.today()).split('-')[1]),int(str(datetime.date.today()).split('-')[2]))
        
        if (today - start_time).days < 1:
            return 0
        if (end_time - start_time).days < 1:
            return 1
        process = (today - start_time).days * 100 / (end_time - start_time).days
        process = 100 if process > 100 else process
        process = 0 if process < 0 else process
        return process

    def healthy(self, uprocess, process):
        if process <= 0:
            return 0
        healthy = int(uprocess)*100/process
        healthy = 100 if healthy > 100 else healthy
        healthy = 0 if healthy < 0 else healthy
        return healthy

    def trancontent(self, content):
        parser = pxfilter.XssHtml()
        parser.feed(content)
        parser.close()
        return parser.getHtml()


    def trandatetime(self, worktime):
        start_time = '-'.join(worktime[:10].split('/'))
        timeArray = time.strptime(start_time, "%m-%d-%Y")
        start_time = time.strftime("%Y-%m-%d", timeArray)
        end_time = '-'.join(worktime[-10:].split('/'))
        timeArray = time.strptime(end_time, "%m-%d-%Y")
        end_time = time.strftime("%Y-%m-%d", timeArray)
        return {'start':start_time, 'end':end_time}


    def is_expired(self, user):
        Modelsdb = models.db.base()
        Modelsdb.db_name = 'report'
        data = Modelsdb.find('[creator] = %s', user['name']).order('[createtime] desc').query()
        if not data:
            return False

        today = datetime.datetime(int(str(datetime.date.today()).split('-')[0]),int(str(datetime.date.today()).split('-')[1]),int(str(datetime.date.today()).split('-')[2]))
        request = datetime.datetime(int(str(user['last_request']).split('-')[0]),int(str(user['last_request']).split('-')[1]),int(str(user['last_request']).split('-')[2]))
        report = datetime.datetime(int(str(user['last_report']).split('-')[0]),int(str(user['last_report']).split('-')[1]),int(str(user['last_report']).split('-')[2]))
        end = datetime.datetime(int(str(user['end_time']).split('-')[0]),int(str(user['end_time']).split('-')[1]),int(str(user['end_time']).split('-')[2]))
        start = datetime.datetime(int(str(user['start_time']).split('-')[0]),int(str(user['start_time']).split('-')[1]),int(str(user['start_time']).split('-')[2]))
        if (today - end).days > 0 or (today - start).days < 0:
            return False
        elif data['isresponsed'] == "否":
            return False
        elif (today - request).days > 0:
            return True
        else:
            return False

    def is_earlier(self, settime):
        today = datetime.datetime(int(str(datetime.date.today()).split('-')[0]),int(str(datetime.date.today()).split('-')[1]),int(str(datetime.date.today()).split('-')[2]))
        time = datetime.datetime(int(str(settime).split('-')[0]),int(str(settime).split('-')[1]),int(str(settime).split('-')[2]))
        if (time - today).days <1:
            return True
        else:
            return False

    def remind(self, user):

        sender = 'forioe@guorunmin.cn'

        message = """From: forioe@guorunmin.cn
To: %s
Subject: 来自进度管理系统的提醒邮件

亲爱的%s
你的导师回复了你的报告并更新了下一次报告的提交时间. 时间未  <b>%s</b>
请留意.
    """ % (user['email'], user['last_request'], user['name'])

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, user['email'], message)   
            print "Successfully sent email"
        except:
            print "Error: unable to send email"






    # def setup_process(self, name):
    #     self.M['student_id'] = self.stuid
    #     self.M['student_name'] = name
    #     self.M['start_time'] = arrow.now().date()
    #     self.M.add()


    # def get_stamp_id(self):
    #     return self.M.find('[student_id] = %s', self.id).fields('id').query()


    # def add_stamp(self, stamp):
    #     stamplist = self.getstamp()
    #     stamplist.append(stamp)
    #     self.updatestamp(stamplist)


    # def is_stamp_exist(self, stamp):
    #     stamplist = self.getstamp()
    #     if stamp in stamplist:
    #         return True
    #     return False


    # def update_stamp(self, stamplist):
    #     M.attr = dict(stamp=stamplist)
    #     M.save('[id] = %s', self.stuid)


    # def del_stamp(self, stamp):
    #     stamplist = self.getstamp()
    #     if stamp not in stamplist:
    #         return False
    #     else:
    #         stamplist.remove(stamp)
    #         self.updatestamp(stamplist)
    #         return True


    # def modify_stamp(self, value):
    #     stamplist = self.getstamp()
    #     if value > stamplist[-1]:
    #         for i in range(stamplist[-1]+1, value+1):
    #             stamplist.append(i)
    #             self.updatestamp(stamplist)
    #     elif value < stamplist[-1]:
    #         if value in stamplist:
    #             while True:
    #                 stamplist.pop()
    #                 if value == stamplist[-1]:
    #                     break
    #             self.updatestamp(stamplist)
    #         else:
    #             stamplist.append(value)
    #             stamplist.sort()
    #             while True:
    #                 stamplist.pop()
    #                 if value == stamplist[-1]:
    #                     break
    #             self.updatestamp(stamplist)

    # def get_stamp(self):
    #     return self.M.find('[student_id] = %s', self.stuid).fields('stamp').query()


    # def get_period(self):
    #     return self.M.find('[student_id] = %s', self.stuid).fields('period').query()


    # def update_period(self, period):
    #     M.attr = dict(period=period)
    #     M.save('[id] = %s', self.stuid)


    # def get_count(self):
    #     return self.M.find('[student_id] = %s', self.stuid).fields('count').query()


    # def update_count(self, count):
    #     M.attr = dict(count=count)
    #     M.save('[id] = %s', self.stuid)



