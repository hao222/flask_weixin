import json
import time

from flask import Blueprint, render_template, request, jsonify, make_response, redirect, g

from common.libs.Helper import render_template_ops
from common.libs.UrlManager import UrlManager
from common.models.User import User
from common.libs.user.UserService import UserService
from web.application import app, db

route_user = Blueprint('user_page', __name__)


@route_user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if g.current_user:
            return redirect(UrlManager.buildUrl("/"))
        return render_template_ops("user/login.html", {'SEO_TITLE':app.config['SEO_TITLE']})
    resp = {'code': 200, 'msg': '登录成功', 'data':{}}
    req = request.values
    login_name = req.get("login_name", '')
    login_pwd = req.get("login_pwd", '')
    if not login_name or len(login_name) < 5:
        resp['code'] = -1
        resp['msg'] = "请输入正确的用户名"
        return jsonify(resp)
    if not login_pwd or len(login_pwd) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入正确的密码"
        return jsonify(resp)

    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "请输入正确的用户名密码"
        return jsonify(resp)
    if user_info.login_pwd != UserService.getPwd(login_pwd, user_info.login_salt):
        resp['code'] = -2
        resp['msg'] = "请输入正确的用户名密码"
        return jsonify(resp)
    if user_info.status !=1:
        resp['code'] = -3
        resp['msg'] = "账号被禁用"
        return jsonify(resp)
    response = make_response(json.dumps(resp))
    # expires=time.time() + 10  设置过期时间 10s
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s"%(UserService.setAuthcode(user_info), user_info.uid))

    return response


@route_user.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        return render_template_ops("user/edit.html", { 'current':'edit' })
    req = request.values
    nickname = req.get("nickname", '')
    email = req.get('email', '')

    resp = {'code': 200, 'msg': '操作成功', 'data':{}}

    if not nickname or len(nickname) < 4:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名~"
        return jsonify(resp)
    if email is None or len(email) < 4:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱~~"
        return jsonify(resp)

    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)


@route_user.route( "/reset-pwd",methods = [ "GET","POST" ] )
def resetPwd():
    if request.method == "GET":
        return render_template_ops( "user/reset_pwd.html",{ 'current':'reset-pwd' } )

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    user_info = g.current_user

    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''

    if user_info.login_pwd != UserService.getPwd(old_password, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = "原密码输入错误~~"
        return jsonify(resp)

    if old_password is None or len( old_password ) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的原密码~~"
        return jsonify(resp)

    if new_password is None or len( new_password ) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的新密码~~"
        return jsonify(resp)

    if old_password == new_password:
        resp['code'] = -1
        resp['msg'] = "请重新输入一个吧，新密码和原密码不能相同哦~~"
        return jsonify(resp)

    user_info = g.current_user

    # if user_info.uid == 1:
    #     resp['code'] = -1
    #     resp['msg'] = "该用户是演示账号，不准修改密码和登录用户名~~"
    #     return jsonify(resp)

    user_info.login_pwd = UserService.getPwd( new_password,user_info.login_salt )

    db.session.add( user_info )
    db.session.commit()
    # 为了防止修改密码后直接退出   更新cookie
    response = make_response(json.dumps( resp ))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (
        UserService.setAuthcode(user_info), user_info.uid), 60 * 60 * 24)  # 保存1天
    return response


@route_user.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/user/login")))
    response.delete_cookie(app.config["AUTH_COOKIE_NAME"])
    return response