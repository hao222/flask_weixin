import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from common.libs.UrlManager import UrlManager


class Application(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        # static_folder 由于自己已经重新定义了 所以这里初始化为None  root_path是为了解决找不到静态路由的
        super(Application, self).__init__(import_name, template_folder=template_folder)
        if "environ" in os.environ:
            self.config.from_pyfile('../config/%s_setting.py' % os.environ['environ'].strip())
        # 此回调可用于初始化用于此数据库设置的应用程序
        db.init_app(self)

db = SQLAlchemy()
app = Application(__name__, template_folder= os.getcwd()+ "/web/templates")

manager = Manager(app)


"""
函数模板
注册自定义模板全局函数
"""

app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
app.add_template_global(UrlManager.buildImageUrl, 'buildImageUrl')
