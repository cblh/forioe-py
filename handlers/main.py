# -*- coding:utf-8 -*-
"""
    @author scoke
    @date 2014-08-19
"""
import os
import re
import sys
import time
import datetime
import lib.web
import configs
import simplejson
import tornado.escape
import models.uc
import models.db
import models.timeline
from lib.web.validators import ObjectDict, xmldatetime, unicode_convert
from lib.web.validators import userstatus, validate_init, IsDate
from lib.process import Process


reload(sys)
sys.setdefaultencoding('utf-8')


class BaseHandler(lib.web.RequestHandler):

    def prepare(self):
        self._prepare_context()
        self._prepare_filters()

    def _prepare_context(self):
        self._context = ObjectDict()
        # self._context.now = datetime.datetime.now()

    def _prepare_filters(self):
        self._filters = ObjectDict()
        self._filters.xmldatetime = xmldatetime
        self._filters.unicode_convert = unicode_convert

    def render(self, template_name, **kwargs):
        kwargs.update(self._filters)
        kwargs["context"] = self._context
        return self.write(self.render_string(template_name, **kwargs))


class MainHandler(BaseHandler):
    # 主页
    @userstatus
    def get(self):
        
        userModel = models.uc.user()
        data = userModel.find('[id] = %s', self.acl_current_user()['id']).query()
        self.set_acl_current_user(data)
        uinfo = self.acl_current_user()
        if uinfo['status'] == '1':
            self.redirect('profile')
            return

        p = Process()  
        if uinfo['status'] == '3':
            data = userModel.get_active_user(uinfo['id'])
            process = {}
            healthy = {}
            for stu in data:
                process[stu['name']] = p.process(stu['start_time'], stu['end_time'])
                healthy[stu['name']] = p.healthy(stu['process'], process[stu['name']])

            self.render('main/index.html', user=uinfo, data=data, process=process,healthy=healthy, isexpired=p.is_expired)

        if uinfo['status'] == '2':
            process = p.process(uinfo['start_time'], uinfo['end_time'])
            healthy = p.healthy(uinfo['process'], process)

            self.render('main/index.html', user=uinfo, data=data, process=process,healthy=healthy, isexpired=p.is_expired)

'''
登陆
'''
class LoginHandler(BaseHandler):

    def get(self):
        self.render('index.html')

    def post(self):
        json = {}
        userModel = models.uc.user()
        username = self.get_argument('username')
        password = self.get_argument('password')
        
        if not username:
            info = {
                'error' : 1,
                'msg' : "请输入用户名"
                }
            self.write(info)
            return
        if not password:
            info = {
                'error' : 1,
                'msg' : "请输入密码"
                }  
            self.write(info)
            return
        data = userModel.find('[name] = %s', username).query()
        if not data:
            json = {
                'error': 1,
                'msg': '用户名或密码错误'
            }
            self.write(json)
            return
        else:
            import hashlib
            m = hashlib.md5()
            m.update(password)


            if m.hexdigest() == data['password']:

                self.set_acl_current_user(data)
                json = {
                    'error': 0,
                    'msg': '/main'
                }
                self.write(json)
                return
            else:
                json = {
                    'error': 1,
                    'msg': '密码错误'
                }
                self.write(json)
                return

'''
退出
'''

class Logout(BaseHandler):

    def get(self):
        self.clear_acl_current_user()
        self.redirect("/")


'''
个人资料
'''
class Profile(BaseHandler):
    @userstatus
    def get(self):
        userModel = models.uc.user()
        data = userModel.find('[id] = %s', self.acl_current_user()['id']).query()
        self.set_acl_current_user(data)
        data = self.acl_current_user()
        teacher = models.uc.user().find('[id] = %s', data['groupid']).query()
        Modelsdb = models.db.base()
        if data['status'] != '3':
            Modelsdb.db_name = 'report'
            report = Modelsdb.find('[creator] = %s', data['name']).count()
            Modelsdb.db_name = 'response'
            response = Modelsdb.find('[towho] = %s', data['name']).count()
            self.render('main/profile.html', teacher=teacher,  user=data, report=report, response=response)
        elif data['status'] == '3':
            Modelsdb.db_name = 'report'
            report = Modelsdb.find('[groupid] = %s', data['id']).count()
            Modelsdb.db_name = 'response'
            response = Modelsdb.find('[groupid] = %s', data['id']).count()
            self.render('main/profile.html', teacher=teacher,  user=data, report=report, response=response)

    @userstatus
    def post(self):
        password = self.get_argument('password')
        confirm = self.get_argument('confirm')
        
        data = {
        'password' : password,
        }
        if not password:
            info = {
                'error' : 1,
                'msg' : "请输入密码"
                }  
            self.write(info)
            return
        if len(password) < 6:
            info = {
                'error' : 1,
                'msg' : "密码长度过低"
                }  
            self.write(info)
            return
        if confirm != password:
            info = {
                'error' : 1,
                'msg' : "两次密码输入不一致"
                }  
            self.write(info)
            return
        info = {
            'error' : 0,
            'msg' : '/main'
            }
        import hashlib
        m = hashlib.md5()
        m.update(password)
        userModel = models.uc.user()
        valuedict = {'password':m.hexdigest()}
        userModel.update(valuedict, 'name',self.acl_current_user()['name'])
        data = userModel.find('[name] = %s', self.acl_current_user()['name']).query()
        self.set_acl_current_user(data)
        self.write(info)


class UserHandler(BaseHandler):
    # 验证学生状态
    @userstatus
    def get(self, studentid):
        if self.acl_current_user()['status'] == '3':
            userModel = models.uc.user()
            data = userModel.find('[id] = %s', studentid).query()
            if data['groupid'] == self.acl_current_user()['id']:
                # process = Process(studentid)
                userModel.attr = dict(status="2")
                userModel.save('[id] = %s', studentid)
                # process.setup_process(data['name'])
                self.redirect('/control')
            else:
                self.redirect('/')
        else:
            self.redirect('/')


    # 注册
    def post(self):
        username = self.get_argument('regiusername')
        password = self.get_argument('regipassword')
        confirm = self.get_argument('regiconfirm')
        
        data = {
        'name' : username,
        'password' : password,
        'status': '0',
        }
        if not username:
            info = {
                'error' : 1,
                'msg' : "请输入用户名"
                }
            self.write(info)
            return
        if not password:
            info = {
                'error' : 1,
                'msg' : "请输入密码"
                }  
            self.write(info)
            return
        if len(password) < 6:
            info = {
                'error' : 1,
                'msg' : "密码长度过低"
                }  
            self.write(info)
            return
        if confirm != password:
            info = {
                'error' : 1,
                'msg' : "两次密码输入不一致"
                }  
            self.write(info)
            return
        userModel = models.uc.user()
        if userModel.find('[name] = %s', username).query():
            info = {
                'error' : 1,
                'msg' : "用户名已被注册"
            }
            self.write(info)
            return
        info = {
            'error' : 0,
            'msg' : '/main'
            }
        import hashlib
        m = hashlib.md5()
        m.update(password)
        userModel = models.uc.user()
        userModel['name'] = username
        userModel['password'] = m.hexdigest()
        userModel.add()      
        userModel.clearAttr() 
        data = userModel.find('[name] = %s', username).query()
        self.set_acl_current_user(data)
        self.write(info)

# 初始化信息
class InitHandler(BaseHandler):
    def get(self):
        if not self.acl_current_user():
            self.redirect('/')
        if self.acl_current_user()['status'] == '3':
            self.redirect('/main')
        self.render('main/init.html', user=self.acl_current_user())

    def post(self):
        if not self.acl_current_user():
            self.redirect('/')
        realname = self.get_argument('name')
        phnum = self.get_argument('phonenum')
        stnum = self.get_argument('stnum')
        teachername = self.get_argument('teachername')
        teachernum = self.get_argument('teachernum')
        email = self.get_argument('email')
        info = validate_init(realname, phnum, stnum, teachername, teachernum, email)
        if info:
            self.write(info)
            if info['error'] == 1:
                return
        userModel = models.uc.user()
        data = userModel.find('[schoolnum] = %s', teachernum).query()
        if data:
            if teachername == data['name']:
                valuedict = dict(
                    realname = realname,
                    schoolnum = str(stnum),
                    phonenum = str(phnum),
                    groupid = data['id'],
                    email = email,
                    status = '1',
                    )
                userModel.update(valuedict, 'name',self.acl_current_user()['name'])
                data = userModel.find('[name] = %s', self.acl_current_user()['name']).query()
                self.set_acl_current_user(data)
                info = {
                'error' : 0,
                'msg' : '/profile'
                }
                self.write(info)
            else:
                info = {
                'error' : 2,
                'msg' : '匹配错误!, 请重新登录',
                'redirect' : '/'
                }
                self.write(info)
        else:
            info = {
            'error' : 0,
            'msg' : '/'
            }
            # self.clear_cookie("user")
            self.write(info)

# 时间轴
class TimeLine(BaseHandler):
    @userstatus
    def get(self):
        tldb = models.timeline.timeline()
        uinfo = self.acl_current_user()
        if uinfo['status'] == '2':
            data = tldb.student_line(uinfo['name'])
            self.render('main/timeline.html', status='2', data=data, user=uinfo)
        elif uinfo['status'] == '3':
            data = tldb.teacher_line(uinfo['id'])
            self.render('main/timeline.html', status='3', data=data, user=uinfo)
        else:
            self.redirect('/profile')
            return

class Report(BaseHandler):
    @userstatus
    def get(self, reportid):
        uinfo = self.acl_current_user()
        Modelsdb = models.db.base()
        Modelsdb.db_name = 'report'
        if reportid == '0':
            if uinfo['status'] == "2":
                data = Modelsdb.find('[creator] = %s', uinfo['name']).order('[createtime] desc').limit(0,100).query()
            elif uinfo['status'] == '3':
                data = Modelsdb.find('[groupid] = %s', uinfo['id']).order('[createtime] desc').limit(0,100).query()
            else:
                self.redirect('/profile')
                return
            self.render('main/report.html', data=data, user=uinfo)
            return
        else:
            data = Modelsdb.find('[id] = %s', reportid).query()
            if data:
                if uinfo['status'] == "3":
                    if data['groupid'] == uinfo['id']:
                        self.render("main/detail.html", data=data, user=uinfo, type='report')
                elif uinfo['status'] == "2":
                    if data['creator'] == uinfo['name']:
                        self.render("main/detail.html", data=data, user=uinfo, type='report')
                else:
                    # self.write({'group':uinfo['groupid'],'id':data['groupid'] })
                    self.redirect('/')

class Response(BaseHandler):
    @userstatus
    def get(self, responseid):
        uinfo = self.acl_current_user()
        Modelsdb = models.db.base()
        Modelsdb.db_name = 'response'
        if responseid == '0':
            if uinfo['status'] == "2":
                data = Modelsdb.find('[towho] = %s', uinfo['name']).order('[createtime] desc').limit(0,100).query()
            elif uinfo['status'] == '3':
                data = Modelsdb.find('[groupid] = %s', uinfo['id']).order('[createtime] desc').limit(0,100).query()
            else:
                self.redirect('/profile')
                return
            self.render('main/response.html', data=data, user=uinfo)
            return
        else:
            data = Modelsdb.find('[id] = %s', responseid).query()
            if data:
                if uinfo['status'] == "2":
                    if data['towho'] == uinfo['name']:
                        self.render("main/detail.html",data=data, user=uinfo, type='response')
                elif uinfo['status'] == '3':
                    if data['groupid'] == uinfo['id']:
                        self.render("main/detail.html",data=data, user=uinfo, type='response')
                else:
                    self.redirect('/')


class Addreport(BaseHandler):
    @userstatus
    def get(self, reportid=None):
        uinfo = self.acl_current_user()
        if uinfo['status'] == '1':
            self.redirect('/')
            return
        if reportid:
            Modelsdb = models.db.base()
            Modelsdb.db_name = 'report'
            if uinfo['status'] == "2":
                self.redirect('/')
            elif uinfo['status'] == '3':
                data = Modelsdb.find('[id] = %s', reportid).query()
                
                if data:
                    userModel = models.uc.user()
                    stu = userModel.find('[name] = %s', data['creator']).query()
                    if data['groupid'] == uinfo['id']:
                        self.render('main/addreport.html', data=data, user=uinfo, stu=stu)
                    else:
                        # self.write({'group':uinfo['id'],'id':data['groupid'] })
                        self.redirect('/')
            # self.render('main/addreport.html', user=uinfo)
        else:
            if uinfo['status'] == '3':
                self.redirect('/')
            self.render('main/addreport.html', user=uinfo)

    @userstatus
    def post(self):
        uinfo = self.acl_current_user()
        p = Process()
        if uinfo['status'] == '1':
            self.redirect('/')
            return
        if uinfo['status'] == '2':
            title = self.get_argument('title')
            content = self.get_argument('content')
            if not title:
                info = {
                    'error' : 1,
                    'msg' : "请输入标题"
                    }  
                self.write(info)
                return
            if len(content) < 20:
                info = {
                    'error' : 1,
                    'msg' : "内容不能少于20字符"
                    }  
                self.write(info)
                return
            else:
                info = {
                'error' : 0,
                'msg' : '/report/0'
                }
                self.write(info)


            content = p.trancontent(content)
            userModel = models.uc.user()

            userdata = userModel.find('[id] = %s', uinfo['id']).query()
            if userdata['last_request'] and userdata['last_report']:
                delay_count = userdata['delay_count'] + 1 if p.is_expired(userdata) else userdata['delay_count']
            else:
                delay_count = userdata['delay_count']
            userModel.attr = dict(last_report=datetime.date.today(), delay_count=delay_count)
            userModel.save('[id] = %s', uinfo['id'])
            userModel.clearAttr()
            Modelsdb = models.db.base()
            Modelsdb.db_name = 'report'
            Modelsdb['title'] = title
            Modelsdb['content'] = content
            Modelsdb['createtime'] = datetime.datetime.today()
            Modelsdb['creator'] = uinfo['name']
            Modelsdb['groupid'] = uinfo['groupid']
            Modelsdb['isresponsed'] = "否"
            Modelsdb.add()
            return

        if uinfo['status'] == '3':
            content = self.get_argument('content')
            reportid = self.get_argument('id')
            title = self.get_argument('title')
            process = self.get_argument('process')
            last_request = self.get_argument('last_request')

            p = Process()
            if not title:
                info = {
                    'error' : 1,
                    'msg' : "请输入标题"
                    }  
                self.write(info)
                return
            if not last_request:
                info = {
                    'error' : 1,
                    'msg' : "请选择日期"
                    }  
                self.write(info)
                return
            if not IsDate(last_request):
                info = {
                    'error' : 1,
                    'msg' : "非法的日期格式"
                    }  
                self.write(info)
                return
            if p.is_earlier(last_request):
                info = {
                    'error' : 1,
                    'msg' : "非法请求, 你无法让学生回到过去去提交报告"
                    }  
                self.write(info)
                return
            if len(content) < 20:
                info = {
                    'error' : 1,
                    'msg' : "内容不能少于20字符"
                    }  
                self.write(info)
                return
            else:
                info = {
                'error' : 0,
                'msg' : '/response/0'
                }
                self.write(info)
            content = p.trancontent(content)
            Modelsdb = models.db.base()
            Modelsdb.db_name = 'report'
            report = Modelsdb.find('[id] = %s', reportid).query()
            Modelsdb.attr = dict(isresponsed="是")
            Modelsdb.save('[id] = %s', reportid)
            Modelsdb.clearAttr()

            userModel = models.uc.user()
            userModel.attr = dict(last_request=last_request, process=process)
            userModel.save('[name] = %s', report['creator'])
            userModel.clearAttr()
            reporter = userModel.find('[name] = %s', report['creator']).query()
            if self.get_argument('remind', defalut='off') != 'off':
                p.remind(reporter)

            Modelsdb.db_name = 'response'    
            Modelsdb['content'] = content
            Modelsdb['createtime'] = datetime.datetime.today()
            Modelsdb['groupid'] = uinfo['id']
            Modelsdb['towho'] = report['creator']
            Modelsdb['toid'] = reportid
            Modelsdb['title'] = title
            Modelsdb.add()
            return

class Control(BaseHandler):
    def get(self):
        uinfo = self.acl_current_user()
        if uinfo['status'] != '3':
            self.redirect('/')
            return
        userModel = models.uc.user()
        data = userModel.get_unactive_user(uinfo['id'])
        student = userModel.get_active_user(uinfo['id'])
        self.render('main/control.html', student=student, data=data, user=uinfo)

    def post(self, studentid):
        p = Process()
        uinfo = self.acl_current_user()
        if uinfo['status'] != '3':
            self.redirect('/')
            return
        worktime = self.get_argument('date-range-picker')
        process = self.get_argument('process')
        if len(worktime) < 20:
            userModel = models.uc.user()
            data = userModel.find('[id] = %s', studentid).query()
            if data['groupid'] == uinfo['id']:
                userModel.attr = dict(process=process)
                userModel.save('[id] = %s', studentid)
                userModel.clearAttr()
                self.redirect('/control')
                # self.write({'starttime':start_time,'endtime':end_time, 'process':process})
        else:
            start_time = p.trandatetime(worktime)['start']
            end_time = p.trandatetime(worktime)['end']
            if start_time == end_time:
                self.redirect('/')
                return 
            
            userModel = models.uc.user()
            data = userModel.find('[id] = %s', studentid).query()
            if data['groupid'] == uinfo['id']:
                userModel.attr = dict(start_time=start_time, end_time=end_time, process=process)
                userModel.save('[id] = %s', studentid)
                userModel.clearAttr()
                self.redirect('/control')
                # self.write({'starttime':start_time,'endtime':end_time, 'process':process})

class Test(BaseHandler):
    def get(self):
        self.render('main/table.html', user=self.acl_current_user())
