# -*- coding: utf-8 -*-
from web.application import app
from common.libs.Helper import render_template_ops
from common.libs.LogService import LogService

@app.errorhandler( 404 )
def error_404( e ):
    LogService.addErrorLog( str(e)  )
    return render_template_ops( 'error/error.html',{ 'status':404,'msg':'很抱歉！您访问的页面不存在' } )