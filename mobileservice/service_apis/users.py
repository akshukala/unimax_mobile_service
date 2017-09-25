'''
    @author = Akshay Kale
    date = 2017-09-25 11:30
'''

from flask import current_app as app
from flask.globals import request
from django.contrib.auth.models import User

from uni_db.mob_app.models import User_Details
from mobileservice.utils.resource import Resource


class UserDetail(Resource):

    def get(self):
        app.logger.info(request)
        return[{
                'user_id': str(user.id),
                'first_name': str(user.user.first_name),
                'last_name': str(user.user.last_name),
                'username': str(user.user.username),
                'password': str(user.password),
                'is_admin': user.is_admin
                } for user in User_Details.objects.filter(is_active=True)[::-1
                                                                          ]]

    def post(self):
        try:
            app.logger.info(request)
            request_data = request.get_json(force=True)
            user_obj = User.objects.create_user(username=str(request_data['u_name']),
                                                password=str(request_data['pwd']))
            user_obj.first_name = str(request_data['f_name']).title()
            user_obj.last_name = str(request_data['l_name']).title()
            user_obj.save()
            status = True if int(request_data['status']) == 1 else False

            User_Details.objects.create(executive_name=str(request_data['f_name']
                                                           ).title() + " " + str(request_data['l_name']).title(),
                                        password=str(request_data['pwd']),
                                        user=user_obj,
                                        is_admin = status
                                        )
            return {
                'responseCode': 200,
                'Message': "User Created Successfully",
            }
        except Exception as e:
            app.logger.debug(str(e))
            return {'responseCode': 503,
                    'Message': "User not Created"}

    def put(self):
        try:
            app.logger.info(request)
            request_data = request.get_json(force=True)
            user_detail_obj = User_Details.objects.get(id=int(request_data['user_id']))
            user = user_detail_obj.user
            user_detail_obj.executive_name = str(request_data['f_name']) + " "\
            + str(request_data['l_name'])
            user_detail_obj.password = str(request_data['pwd'])
            user_detail_obj.save()
            user.set_password(str(request_data['pwd']))
            user.username = str(request_data['u_name'])
            user.first_name = str(request_data['f_name'])
            user.last_name = str(request_data['l_name'])
            user.save()
            return {
                'responseCode': 200,
                'Message': "User Updated Successfully",
            }
        except Exception as e:
            app.logger.debug(str(e))
            return {'responseCode': 503,
                    'Message': "User not Updated"}

    def delete(self):
        try:
            app.logger.info(request)
            request_data = request.get_json(force=True)
            User_Details.objects.filter(id=int(request_data['user_id'])
                                        ).update(is_active=False)
            return {
                'responseCode': 200,
                'Message': "User Deleted Successfully",
            }
        except Exception as e:
            app.logger.debug(str(e))
            return {'responseCode': 503,
                    'Message': "User not Deleted"}
