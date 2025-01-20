from flask_restx import Api

from bapp import __version__
from bapp.core.exception import BaseApiException

# 实例化API
api = Api(version=__version__, title='Beancount REST API', description='A REST API for Beancount')


# 注册异常处理
@api.errorhandler(BaseApiException)
def handle_exception(error):
    return {'message': str(error)}, 400
