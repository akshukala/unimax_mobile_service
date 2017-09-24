'''
    @author = Akshay Kale
    date = 2017-06-16 15:34
'''

from flask import current_app as app
from flask.globals import request

from uni_db.mob_app.models import User_Details
from mobileservice.utils.resource import Resource


class UserDetail(Resource):

    def get(self):
        return[{
                'username': str(user.user.username),
                'password': str(user.password),
                'is_admin': user.is_admin
                } for user in User_Details.objects.filter(is_active=True)]