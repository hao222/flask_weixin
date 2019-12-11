import time

# from web.application import app


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl( path ):
        return path

    @staticmethod
    def buildStaticUrl(path):
        release_version = ""
        ver = "%s"%( int(time.time()) ) if not release_version else release_version
        path =  "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl( path )

    @staticmethod
    def buildImageUrl(path):
        # app_config = app.config['APP']
        url = "http://127.0.0.1:5005/static/upload/" + path
        return url