# -*- coding:utf-8 -*-

import sys
from lib.web.validators import make_cookie_secret
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado import web
import configs
import os
import multiprocessing


class Application(web.Application):

        def __init__(self):
            from urls import handlers

            settings = {
                'debug': True,
                #'cookie_secret': make_cookie_secret(),
                'cookie_secret': 'asadewrfds1',
                #'gzip': True,
                'xsrf_cookies': False,
                'root_path': os.path.dirname(__file__),
                'template_path': os.path.join(os.path.dirname(__file__), "templates"),
                'static_path': os.path.join(os.path.dirname(__file__), "static"),
                'acl': {
                    'db_name': 'uc_role',  # 存放 role 的表名
                },
                'session': {
                    'store': 'Redis',  # session 的存放方式
                    'args': {}  # 附加参数
                },
                'login_url' : "/",
                # 'ui_modules': ui_modules,
            }
            super(Application, self).__init__(handlers, **settings)
            Application.cache = configs.cache_Connection


if __name__ == '__main__':

    # try:
    #     port = int(sys.argv[1])
    # except Exception, e:
    #     port = configs.http_port

    def run(mid, port):
        print "Process %d start" % mid
        server = HTTPServer(Application())
        server.listen(port)
        IOLoop.instance().start()
    jobs=list()
    for mid,port in enumerate(range(45679,45699)):
        p=multiprocessing.Process(target=run,args=(mid,port))
        jobs.append(p)
        p.start()
    # server = HTTPServer(Application())
    # server.listen(port)
    # print "server listening on 0.0.0.0:%s" % port
    # IOLoop.instance().start()

