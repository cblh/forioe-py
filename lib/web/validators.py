# -*- coding:utf-8 -*-
import types
import re
import time
import httplib
import urllib
import base64
import uuid
import os
import configs
import smtplib  
from email.mime.text import MIMEText  
from email.Header import Header
from random import Random
import random
import models.uc

class ObjectDict(dict):

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value



def validate_init(realname, phnum, stnum, teachername, teachernum, email):
    if not realname:
        info = {
            'error' : 1,
            'msg' : "请输入姓名"
            }  
        return info
    if not IsChineseChar(realname):
        info = {
            'error' : 1,
            'msg' : "非法的姓名格式"
        }
        return info
    if len(realname) < 2:
        info = {
            'error' : 1,
            'msg' : "非法的姓名格式"
        }
        return info
    if not phnum:
        info = {
            'error' : 1,
            'msg' : "请输入手机号"
            }  
        return info
    if len(phnum) != 11:
        info = {
            'error' : 1,
            'msg' : "手机号输入不正确"
            }  
        return info
    if not phnum.isdigit():
        info = {
            'error' : 1,
            'msg' : "非法的手机号码"
        }
        return info
    if not stnum:
        info = {
            'error' : 1,
            'msg' : "请输入学号"
            }  
        return info
    if len(stnum) != 11:
        info = {
            'error' : 1,
            'msg' : "学号输入不正确"
            }  
        return info
    if not stnum.isdigit():
        info = {
            'error' : 1,
            'msg' : "非法的学号"
        }
        return info
    if not IsEmail(email):
        info = {
            'error' : 1,
            'msg' : "非法的邮件地址"
        }
        return info
    if not teachername:
        info = {
            'error' : 1,
            'msg' : "请输入导师姓名"
            }  
        return info
    if not teachernum:
        info = {
            'error' : 1,
            'msg' : "请输入导师工号"
            }  
        return info
    

def userstatus(func):
    def wrap(self, *args, **kwargs):
        userModel = models.uc.user()
        if not self.acl_current_user():
            self.redirect('/')
            return
        data = userModel.find('[name] = %s', self.acl_current_user()['name']).query()
        if data['status'] == '0' or not data['groupid']:
            self.redirect('/init')
            return
        return func(self, *args, **kwargs)
    return wrap


# 判断是否为整数 15
def IsNumber(varObj):

    if False == type(varObj) is int:
        return str(varObj).isdigtal()
    return True

# 判断是否为字符串 string


def IsString(varObj):

    return isinstance(varObj, bytes)

# 判断是否为浮点数 1.324


def IsFloat(varObj):
    return isinstance(varObj, float)

# 判断是否为字典 {'a1':'1','a2':'2'}


def IsDict(varObj):

    return isinstance(varObj, dict)

# 判断是否为tuple [1,2,3]


def IsTuple(varObj):

    return isinstance(varObj, tuple)

# 判断是否为List [1,3,4]


def IsList(varObj):

    return isinstance(varObj, list)

# 判断是否为布尔值 True


def IsBoolean(varObj):

    return isinstance(varObj, bool)

# 判断是否为货币型 1.32


def IsCurrency(varObj):

    # 数字是否为整数或浮点数
    if IsFloat(varObj) and IsNumber(varObj):
        # 数字不能为负数
        if varObj > 0:
            return isNumber(currencyObj)
            return False
    return True

# 判断某个变量是否为空 x


def IsEmpty(varObj):

    if len(varObj) == 0:
        return True
    return False

# 不为空


def NotEmpty(varObj):
    if IsNone(varObj):
        return False
    if IsEmpty(varObj):
        return False
    return True

# 判断变量是否为None None


def IsNone(varObj):
    return isinstance(varObj, type(None))  # == "None" or varObj == "none":

# 判断是否为日期格式,并且是否符合日历规则 2010-01-31


def IsDate(varObj):

    if len(varObj) == 10:
        rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
        match = re.match(rule, varObj)
        if match:
            return True
        return False
    return False

# 判断是否为邮件地址


def IsEmail(varObj):

    rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
    match = re.match(rule, varObj)

    if match:
        return True
    return False

# 判断是否为中文字符串


def IsChineseCharString(varObj):

    for x in varObj:
        if (x >= u"\u4e00" and x <= u"\u9fa5") or (x >= u'\u0041' and x <= u'\u005a') or (x >= u'\u0061' and x <= u'\u007a'):
            continue
        else:
            return False
    return True


# 判断是否为中文字符
def IsChineseChar(varObj):

    if varObj[0] > chr(127):
        return True
    return False

# 判断帐号是否合法 字母开头，允许4-16字节，允许字母数字下划线


def IsLegalAccounts(varObj):

    rule = '[a-zA-Z][a-zA-Z0-9_]{3,15}$'
    match = re.match(rule, varObj)

    if match:
        return True
    return False


# 匹配IP地址
def IsIpAddr(varObj):

    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, varObj):
        return False
    else:
        return True


def regex(pattern, data, flags=0):
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern, flags)

    return pattern.match(data)


def email(data):
    pattern = r'^.+@[^.].*\.[a-z]{2,10}$'
    return regex(pattern, data, re.IGNORECASE)


def ip(data):
    pattern = r'((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)'
    return regex(pattern, data, re.IGNORECASE)


def xmldatetime(value):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(value)))

def xmldatetimeym(value):
    return time.strftime('%Y-%m', time.localtime(int(value)))

def xmldatetimeymd(value):
    return time.strftime('%Y-%m-%d', time.localtime(int(value)))

def xmldatetimey(value):
    return time.strftime('%Y', time.localtime(int(value)))

def xmldatetimed(value):
    return time.strftime('%d', time.localtime(int(value)))

def xmldatetimeh(value):
    return time.strftime('%H', time.localtime(int(value)))


def make_cookie_secret():
    return base64.b64encode(
            uuid.uuid4().bytes + uuid.uuid4().bytes)



def unicode_convert(t):
    if t:
        pattern = re.compile('\\\\u[0-9a-f]{4}')
        t_all = pattern.findall(t)

        if t_all:
            for o in t_all:
                n = unichr(eval('0x'+o.replace('\\u', '')))
                t = t.replace(o, n)
    return t









