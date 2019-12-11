
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/food_db'

SERVER_PORT = "5005"

SQLALCHEMY_TRACK_MODIFICATIONS = True

AUTH_COOKIE_NAME = "food_"

# 过滤url
IGNORE_URLS = [
    "^/user/login",
    "^/api"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico",
    "^/apidoc/"
]

API_IGNORE_URLS = [
    "^/api"
]

# 每页展示
PAGE_SIZE =10
# 默认显示多少页
PAGE_DISPLAY = 10


STATUS_MAPPING = {
    "1": "正常",
    "0":"已删除"
}

API_SECRET = '816757fe4332c54b4078a07f8d9376c0'
APPID = 'wxd3945bbe5dea923c'

MINA_APP = {
    'appid':'wxd3945bbe5dea923c',
    'appkey':'816757fe4332c54b4078a07f8d9376c0',
    'paykey': 'asfg324534td',  # 微信支付秘钥
    'mch_id': '11100010',    # 商家号
    'callback_url': '/api/order/callback'
}


UPLOAD = {
    'ext': ['jpg', 'gif', 'jpeg', 'png'],
    'prefix_path': '/static/upload/',
    # 默认配置的静态文件
    'prefix_url':'/static/upload/'
}

APP = {
    'domain': 'http://127.0.0.1:5005'
}

PAY_STATUS_MAPPING = {
    "1":"已支付",
    "-8":"待支付",
    "0":"已关闭"
}


PAY_STATUS_DISPLAY_MAPPING = {
    "0":"订单关闭",
    "1":"支付成功",
    "-8":"待支付",
    "-7": "待发货",
    "-6":"待确认",
    "-5":"待评价"
}