from models import db

class timeline(db.base):
    def __init__(self):
        db.base.__init__(self)

    def student_line(self, name):
        return self.query('select [title],[id],[content],[createtime],[creator] from [report] where [creator]=%s union select [title],[id],[content],[createtime],[groupid] from [response] where [towho]=%s order by [createtime] desc', name, name)

    def teacher_line(self, uid):
    	return self.query('select [title],[id],[content],[createtime],[creator],[groupid] from [report] where [groupid]=%s union select [title],[id],[content],[createtime],[groupid],[towho] from [response] where [groupid]=%s order by [createtime] desc', uid, uid)