# -*- coding:utf-8 -*-
import tornado.escape
import uuid
import time
import configs
import models.db
import models.uc
import functools
import tornado.web
import redis
from tornado.web import HTTPError
'''
== Session 类 ==
# 每个会话有效期最长为1天
# 在实例化时,可指定ID, 没有指定时,生成一个32位的id

=== API : ===
# session = new Session()
# session.id() # 取 session id
# session.set( key , value )
# session.get( key )
# session.delete( key )
# session.clear() # 清空session

# session[key]
# session[key] = value
# for k in session.keys()
# del session[key]

'''


class Session:

    def __init__(self, session_id=None, store='Redis', args={}):

        self.store = Session_Store_Rediscache()

        self.time = 1800
        if session_id:
            self.session_id = session_id
        else:
            self.session_id = self._generate_session_id()

    def _generate_session_id(cls):
        return str(uuid.uuid4())

    # 返回 session id
    def id(self):
        return self.session_id

    # 设置session
    def set(self, key, value):
        self.store.set(self.session_id, key, value, self.time)

    # 取值
    def get(self, key):
        return self.store.get(self.session_id, key)

    # 删除值
    def delete(self, key):
        self.store.delete(self.session_id, key)

    # 清空
    def clear(self):
        self.store.clear(self.session_id)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, key):
        return self.delete(key)

    def __len__(self):
        return len(self.data.keys())

    def __str__(self):
        return self.data

    def keys(self):
        return self.data.keys()

# 将session放入 redis


class Session_Store_Rediscache:

    def __init__(self):
        self.mc = redis.Redis(
            host=configs.redis_host,
            port=configs.redis_port,
            db=configs.redis_db)

    def get(self, session_id, key):
        data = self.get_data(session_id)
        if not data:
            return None
        if key in data['values']:
            return data['values'][key]
        return None

    def clear(self, session_id):
        self.mc.delete(session_id)

    def delete(self, session_id, key):
        data = self.get_data(session_id)
        if data and key in data['values']:
            del data['values'][key]

            session = {
                'values': data['values'],
                'session_time': int(time.time()),
                'left_time': data['left_time']
            }

            self.mc.set(session_id, tornado.escape.json_encode(session))
            self.mc.expire(session_id, int(data['left_time']))

    def set(self, session_id, key, value, left_time=1800):
        data = self.get_data(session_id)
        if not data:
            data = {'values': {}}

        data['values'][key] = value

        session = {
            'values': data['values'],
            'session_time': int(time.time()),
            'left_time': int(left_time)
        }

        self.mc.set(session_id, tornado.escape.json_encode(session))
        self.mc.expire(session_id, int(left_time))

    def get_data(self, session_id):
        data = self.mc.get(session_id)
        if not data:
            return False
        data = tornado.escape.json_decode(data)

        # 超时,删除
        if time.time() > (data['session_time'] + data['left_time']):

            email = data['values']['current_user']['email']
            userModel = models.uc.user()
            userModel.attr = {'status': 0}
            userModel.save('[email] = %s', email)
            self.clear(session_id)
            return False

        # 更新时间 , 离结束还有 10 秒, 更新生命周期
        if time.time() > (data['session_time'] + data['left_time'] - 10):
            data['session_time'] = int(time.time())
            self.mc.set(session_id, tornado.escape.json_encode(data))
            self.mc.expire(session_id, int(data['left_time']))
        return data

'''
== 将 Session 加入 RequestHandler ==

=== api ===
# get_session
# set_session

=== 注: ===
# 调用 self._session_Instance() ,可直接访问 self._session
# self._session 支持字典属性
# self._session['key'] , self._session['key'] = 'val'
# for k in self._session.keys()
'''


class RequestHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        self._start_time = time.time()
        tornado.web.RequestHandler.__init__(
            self, application, request, **kwargs)

    # 数据库连接
    @property
    def db(self):
        return models.db.base()

    def db_method(self):
        return models.db.base()

    # 缓存
    @property
    def cache(self):
        return self.application.cache

    # 取session实例
    def session(self):
        # session 已经实例化,直接返回
        if hasattr(self, ' _session'):
            return self._session

        if self.get_secure_cookie('PYSESSID'):
            self._session = Session(
                self.get_secure_cookie('PYSESSID'),
                self.settings['session']['store'],
                self.settings['session']['args'])
        else:
            self._session = Session(
                False,
                self.settings['session']['store'],
                self.settings['session']['args'])
            self.set_secure_cookie('PYSESSID', self._session.id())

        return self._session

    # 显示错误信息
    def error(self, **args):
        args['url'] = 'url' in args and args['url'] or self.request.path
        return self.render("admin/error.html", **args)

        # 取session值
    def get_session(self, key):
        return self.session().get(key)

    # 设置session值
    def set_session(self, key, val):
        self.session().set(key, val)

    # 访问被拒绝时的错误处理函数
    def _on_access_denied(self, msg='403 禁止访问', url='/login'):
        self.error(msg=msg, url=url)
        # raise HTTPError(403)

    # 设置当前用户acl信息
    def set_acl_current_user(self, info):
        user_info = info
        # user_info['roles'] = roles
        self.session().set('current_user', user_info)

    # 取当前用户acl信息
    def acl_current_user(self):
        current_user = self.session().get('current_user')
        if not current_user:
            return {}
        return current_user

    # 清空当前用户acl信息
    def clear_acl_current_user(self):
        self.session().delete('current_user')

    def request_time(self):
        """Returns the amount of time it took for this request to execute."""
        return time.time() - self._start_time


class ApiHandler(RequestHandler):

    def write(self, chunk):
        if isinstance(chunk, dict):
            chunk = tornado.escape.json_encode(chunk)
            callback = self.get_argument('callback', None)
            if callback:
                chunk = "%s{%s}" % (callback, tornado.escape.to_unicode(chunk))
            self.set_header(
                "Content-Type",
                "application/javascript; charset=UTF-8")
        super(ApiHandler, self).write(chunk)

# 实现 ACL 访问控制


def acl(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):

        # 取当前用户
        if None == method.func_defaults:
            return self._on_access_denied('内部错误,模块权限参数未配置')
        else:
            if 1 != len(method.func_defaults):
                return self._on_access_denied('内部错误,获取模块参数失败')
            else:
                model = method.func_defaults[0]

        current_user = self.acl_current_user()
        if current_user:
            if current_user['roles'] != 0:
                roles = current_user['roles'][0]
            else:
                return self._on_access_denied('该用户角色未分配,请联系管理员')
        else:
            uri = '/login?next=%s' % self.request.uri
            return self.redirect(uri)

        _config = self.settings['acl']
        ruleCache = self.cache.get(configs.cache_role_name + roles)
        if not ruleCache:
            db = self.db_method().table(_config['db_name'])
            role = eval(db.find('[name] = %s',roles).fields('[perarr]').query()['perarr'])
            if role:
                self.cache.set(configs.cache_role_name + roles, role)
        else:
            role = eval(ruleCache)

        if model not in role:
            return self._on_access_denied('sorry,您没有当前地址访问权限')

        return method(self, *args, **kwargs)
    return wrapper

def competence(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):

        if None == method.func_defaults:
            return self._on_access_denied('内部错误,模块权限参数未配置')
        else:
            if 1 != len(method.func_defaults):
                return self._on_access_denied('内部错误。获取模块参数失败')
            else:
                model = method.func_defaults[0]

        roles = self.acl_current_user()['roles'][0]

        _config = self.settings['acl']
        ruleCache = self.cache.get(configs.cache_role_name + roles)

        if not ruleCache:
            db = self.db_method().table(_config['db_name'])
            role = eval(db.find('[name] = %s', roles).fields('[perarr]').query()['perarr'])
            if role:
                self.cache.set(configs.cache_role_name + roles, role)
        else:
            role = eval(ruleCache)

        if model not in role:
            json = {
                'error': 1,
                'msg': '很抱歉,您没有该权限'
            }
            self.write(json)
            return

        return method(self, *args, **kwargs)
    return wrapper

class UIModule(tornado.web.UIModule):

    # 数据库连接
    def db(self):
        return models.db.base()

    @property
    def cache(self):
        return self.handler.cache

