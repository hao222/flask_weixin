from werkzeug.utils import secure_filename

from common.libs.Helper import getCurrentDate
from common.models.Image import Image
from web.application import app, db
import os,stat, uuid

class UploadService():

    @staticmethod
    def uploadByFile(file):
        config_ext = app.config['UPLOAD']
        resp = {'code':200, 'msg':'操作成功', 'data':{}}
        # 获取安全的文件名字
        filename = secure_filename(file.filename)
        ext = filename.rsplit(".", 1)[1]    # 扩展
        if ext not in config_ext['ext']:
            resp['code'] = -1
            resp['msg'] = '不允许扩展类型文件'
            return resp
        root_path = app.root_path + config_ext['prefix_path']
        file_dir = getCurrentDate("%Y%m%d")
        save_dir = root_path+file_dir
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
            os.chmod(save_dir, stat.S_IRWXG|stat.S_IRGRP| stat.S_IRWXO)
        file_name = str(uuid.uuid4()).replace("-", "")+ '.' + ext
        file.save("{0}/{1}".format(save_dir, file_name))

        # 存储上传的文件  保存到数据库中 为了实现ueditor listimage在线管理

        model_image = Image()
        model_image.file_key = file_dir + "/" + file_name
        model_image.created_time = getCurrentDate()
        db.session.add(model_image)
        db.session.commit()

        resp['data'] = {
            'file_key': model_image.file_key
        }
        return resp