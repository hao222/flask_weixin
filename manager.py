from jobs.launcher import runJob
from web.application  import app, manager

from flask_script import Server, Option
# 在入口文件处 导入蓝图
import web.www
# web server
# Server flask开发服务器
manager.add_command("runserver", Server( port=app.config["SERVER_PORT"], use_debugger=True, use_reloader=True))


# job 处理异步消息
manager.add_command("runjob", runJob())

def main():
    manager.run()


if __name__ == "__main__":
    try:
        import sys
        sys.exit( main() )

    except Exception as e:
        import traceback
        traceback.print_exc()


# flask_script    管理启动规范化