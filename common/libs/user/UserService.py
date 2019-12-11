
import hashlib,base64
import random,string


class UserService():
    """
    getPwd: 生成加盐的密码
    setAuthcode： 生成验证的cookie
    setSalt： 生成加盐
    """
    @staticmethod
    def getPwd(pwd, salt):
        m = hashlib.md5()
        str = "%s-%s"%(base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def setAuthcode(user_info):
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt )
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def setSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return "".join(keylist)