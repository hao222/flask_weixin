from flask import Blueprint, render_template, send_from_directory
from web.application import app

# static.py 是为了 防止静态文件找不到
route_static = Blueprint('static', __name__)

@route_static.route("/<path:filename>")
def index(filename):
    return send_from_directory(app.root_path + "web/static/", filename)