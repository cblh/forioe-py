# from handler.home import HomeHandler
# from handler.home import Detail
# from handler.home import Guestcate
# from handler.admin import Login
# from handler.admin import Blog

# from handler.admin import Modify
# from handler.admin import Delete
# from handler.admin import Category
# from handler.admin import User
# from handler.admin import AdminHandler
# from handler.admin import Delete_user
# from handler.admin import Password

from handlers.main import UserHandler
from handlers.main import LoginHandler
# from handlers.main import HomeHandler
from handlers.main import MainHandler
from handlers.main import TimeLine
from handlers.main import Report
from handlers.main import Response
from handlers.main import Profile
from handlers.main import Addreport
# from handlers.main import Detail
from handlers.main import InitHandler
from handlers.main import Logout
from handlers.main import Control

from handlers.main import Test


handlers = [
        # (r"/", HomeHandler),
        # (r"/login", Login),
        # (r"/admin", AdminHandler),
        (r"/logout", Logout),
        # (r"/modify/([0-9].*)", Modify),
        # (r"/modify", Modify),
        # (r"/blog/([0-9].*)", Detail),
        # (r"/admin/blog/delete/([0-9].*)", Delete),
        # (r"/admin/category/([0-9a-zA-Z].*)", Category),
        # (r"/admin/category", Category),
        # (r"/category/([0-9].*)", Guestcate),
        # (r"/admin/user", User),
        # (r"/admin/blog", Blog),
        # (r"/admin/delete/user/([0-9].*)", Delete_user),
        # (r"/admin/profile", Password),
        (r"/user", UserHandler),
        (r"/user/([0-9].*)", UserHandler),
        (r"/", LoginHandler),
        # (r"/", HomeHandler),
        (r"/main", MainHandler),
        (r"/timeline", TimeLine),
        (r"/report/([0-9].*)", Report),
        (r"/response/([0-9].*)", Response),
        (r"/profile", Profile),
        (r"/addreport", Addreport),
        (r"/addreport/([0-9].*)", Addreport),
        # (r"/detail/([0-9].*)", Detail),
        (r"/init", InitHandler),
        (r"/control", Control),
        (r"/control/([0-9].*)", Control),
        (r"/test", Test),
        ]
