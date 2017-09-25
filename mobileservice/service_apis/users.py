'''
    @author = Akshay Kale
    date = 2017-06-16 15:34
'''

from flask import current_app as app
from flask.globals import request
from django.contrib.auth.models import User

from uni_db.mob_app.models import User_Details
from mobileservice.utils.resource import Resource


class UserDetail(Resource):

    def get(self):
        return[{
                'user_id': str(user.id),
                'first_name': str(user.user.first_name),
                'last_name': str(user.user.last_name),
                'username': str(user.user.username),
                'password': str(user.password),
                'is_admin': user.is_admin
                } for user in User_Details.objects.filter(is_active=True)]

    def post(self):
        try:
            request_data = request.get_json(force=True)
            user_obj = User.objects.create_user(username=str(request_data['u_name']),
                                                password=str(request_data['pwd']))
            user_obj.first_name = str(request_data['f_name']).title()
            user_obj.last_name = str(request_data['l_name']).title()
            user_obj.save()
            User_Details.objects.create(executive_name=str(request_data['f_name']
                                                           ).title() + " " + str(request_data['l_name']).title(),
                                        password=str(request_data['pwd']),
                                        user=user_obj
                                        )
            return {
                'responseCode': 200,
                'Message': "User Created Successfully",
            }
        except Exception as e:
            app.logger.debug(str(e))
            return {'responseCode': 503,
                    'Message': "User not Created"}
