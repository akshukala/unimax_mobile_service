from flask import current_app as app
from flask.globals import request
from flask_restful import Resource
import cloudinary
import cloudinary.uploader
import cloudinary.api
from __builtin__ import file

from uni_db.mob_app.models import Shop_Images

class Cust_Image(Resource):

    def post(self):
        print "Hello"
        file = request.files['image']
        data = request.values.to_dict()
        print file
        print data
#         cloudinary.config(cloud_name="http-nimbrisk-com",
#                           api_key="854195629923224",
#                           api_secret="swPL_-5N9bzrMZWZofMi95b5wCM")
# 
#         response = cloudinary.uploader.upload(request.FILES['image'])
#         print response
        return{
                    'responseCode': 200,
                    'Message': "Image Uploaded Successfully."
                }
