from flask.globals import request
from flask_restful import Resource
import cloudinary.uploader

from __builtin__ import file

from uni_db.mob_app.models import Shop_Images, Customer


class Cust_Image(Resource):

    def post(self):
        file = request.files['image']
        data = request.values.to_dict()
        cloudinary.config(cloud_name="http-nimbrisk-com",
                          api_key="854195629923224",
                          api_secret="swPL_-5N9bzrMZWZofMi95b5wCM")

        response = cloudinary.uploader.upload(file, crop='limit',
                                              width=512,
                                              height=512,
                                              eager=[{'width': 100,
                                                      'height': 150,
                                                      'crop': 'fill'}])
        Shop_Images.objects.create(img_url=str(response['secure_url']),
                                   customer=Customer.objects.get(id=int(data['customer_id'])))
        return{
                    'responseCode': 200,
                    'Message': "Image Uploaded Successfully."
                }
