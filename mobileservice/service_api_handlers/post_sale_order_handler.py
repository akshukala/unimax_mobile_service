from flask import current_app as app
import requests
import json
import cloudinary.uploader

from uni_db.mob_app.models import (CustOrder, Order_Item, Customer,
                                   Shop_Images, FirebaseToken)
from mobileservice.utils.auth import get_user


def handle_request(request_data, files):
    try:
        print request_data
        print files
        '''Creating Customer and saving'''
        cust_obj = Customer.objects.create(shop_name=str(request_data['shop_name']).title(),
                                           person_name=str(request_data['cust_name']).title(),
                                           contact_no=str(request_data['contact']),
                                           area=str(request_data['area']
                                                    ).title(),
                                           created_by=get_user(),
                                           modified_by=get_user())
        if request_data['addr']:
            cust_obj.address = str(request_data['addr'])
        if request_data['gst']:
            cust_obj.gst_no = str(request_data['gst'])
        if request_data['pan']:
            cust_obj.pan_no = str(request_data['pan'])
        cust_obj.save()
        '''Creating Order and saving it.'''
        order_obj = CustOrder.objects.create(owner=cust_obj,
                                             payment_type=int(request_data['pay_type']),
                                             created_by=str(get_user().username),
                                             modified_by=str(get_user().username),
                                             grand_total=float(request_data['total']))
        if request_data['remark']:
            order_obj.remarks = str(request_data['remark'])
        order_obj.save()
        '''Creating orderitems and saving it'''
        items = str(request_data['itemname']).split('$')
        qty = (request_data['qty']).split('$')
        price = (request_data['item_price']).split("$")
        for itr in range(0, len(items)-1):
            temp = float(price[itr])/int(qty[itr])
            Order_Item.objects.create(order=order_obj, item_name=items[itr],
                                      quantity=int(qty[itr]),
                                      selling_price=temp,
                                      total_price=float(price[itr]))
        '''Cloudinary Credentials'''
        cloudinary.config(cloud_name="http-nimbrisk-com",
                          api_key="854195629923224",
                          api_secret="swPL_-5N9bzrMZWZofMi95b5wCM")
        '''Saving images on cloud'''
        for file in files.values():
            response = cloudinary.uploader.upload(file, crop='limit',
                                                  width=512,
                                                  height=512,
                                                  eager=[{'width': 200,
                                                          'height': 200,
                                                          'crop': 'fill'}])
            Shop_Images.objects.create(img_url=str(response['secure_url']),
                                       customer=cust_obj)

        title = "Order Created By " + str(order_obj.created_by)
        desc = "Order of amount Rs " + str(request_data['total']) + " has been created."
        token_list = [str(obj.token_id) for obj in FirebaseToken.objects.all()]
        API_ACCESS_KEY = 'AIzaSyCoFp3hp-ypjISBbn3ms96dCq4aYFkuWTY'
        registrationIds = token_list
        url = 'https://android.googleapis.com/gcm/send'
        fields = {
            'registration_ids': registrationIds,
            "data": {
              "name": "Unimax Enterprises",
              "body": desc,
              "title": title
            }
        }

        # Adding empty header as parameters are being sent in payload
        headers = {'Authorization': 'key=' + API_ACCESS_KEY,
                   'Content-Type': 'application/json'}
        result = requests.post(url, data=json.dumps(fields), headers=headers)
        return {
                'responseCode': 200,
                'Message': "Order saved",
                'order_id': str(order_obj.id),

            }
    except Exception as e:
            app.logger.debug(str(e))
            return {'responseCode': 500,
                    'Message': "Order not saved"}