from uni_db.settings.pool import init_pool
from os.path import dirname, abspath

import django
from django.db import close_old_connections
from flask import Flask
from flask.ext import restful


from mobileservice.conf.config_logger_setup import setup_config_logger
from mobileservice.session.interfaces import DBInterface
from flask.ext.cors import CORS

from mobileservice.service_apis.ping import Ping
from mobileservice.service_apis.sale_order import SaleOrder
from mobileservice.service_apis.users import UserDetail
from mobileservice.service_apis.images import Cust_Image
from mobileservice.service_apis.firebase_token import Token
from mobileservice.service_apis.notification import Send_Notification

close_old_connections()
init_pool()

django.setup()
app = Flask(__name__)
CORS(app)
app.auth_header_name = 'X-Authorization-Token'
app.session_interface = DBInterface()
app.root_dir = dirname(dirname(abspath(__file__)))

api = restful.Api(app)

setup_config_logger(app)

app.logger.info("Setting up Resources")
api.add_resource(Ping, '/mobileservice/ping/')
api.add_resource(SaleOrder, '/mobileservice/sale_order/')
api.add_resource(UserDetail, '/mobileservice/user_detail/')
api.add_resource(Cust_Image, '/mobileservice/images/')
api.add_resource(Token, '/mobileservice/fcm_token/')
api.add_resource(Send_Notification, '/mobileservice/notification/')

app.logger.info("Resource setup done")

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=7291, threaded=True)
