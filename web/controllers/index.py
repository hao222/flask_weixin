import datetime

from flask import Blueprint, render_template,g

from common.libs.Helper import render_template_ops, getFormatDate
from common.models.stat.StatDailySite import StatDailySite

route_index = Blueprint('index_page', __name__)


@route_index.route("/")
def index():
    ##
    # 为了不让每一个页面都传current_user 我们需要修改 render_template  libs 下创建helper文件 统一使用新的render_template
    ###
    resp_data = {
        'data':{
            "finance":{
                "today":0,
                "month":0
            },
            "member":{
                "today_new":0,
                "month_new":0,
                "total":0
            },
            "order":{
                "today":0,
                "month":0,
            },
            "shared":{
                "today":0,
                "month":0
            }
        }
    }
    now = datetime.datetime.now()
    date_before_30day = now + datetime.timedelta(days=-30)
    date_from = getFormatDate(date=date_before_30day, format="%Y-%m-%d")
    date_to = getFormatDate(date=now, format="%Y-%m-%d")

    list = StatDailySite.query.filter(StatDailySite.date >= date_from)\
        .filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()).all()
    data = resp_data['data']
    if list:
        for item in list:
            data['finance']['month'] += item.total_pay_money
            data['member']['month_new'] += item.total_new_member_count
            data['member']['total'] = item.total_member_count

            data['order']['month'] += item.total_order_count
            data['shared']['month'] += item.total_shared_count

            if getFormatDate(date=item.date, format="%Y-%m-%d") == date_to:
                data['finance']['today'] = item.total_pay_money
                data['member']['today'] = item.total_new_member_count
                data['order']['today'] = item.total_order_count
                data['shared']['today'] = item.total_pay_money
    return render_template_ops("index/index.html", resp_data)