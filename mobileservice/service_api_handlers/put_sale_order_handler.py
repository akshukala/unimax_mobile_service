from django.core.exceptions import ObjectDoesNotExist
from flask import current_app as app

from uni_db.mob_app.models import CustOrder, Order_Item, Customer
from mobileservice.utils.auth import get_user


def handle_request(response_data):
    print response_data
    try:
        order_obj = CustOrder.objects.get(id=int(response_data['order_id'])
                                          ).select_related('owner')
        cust_obj = order_obj.owner
        cust_obj.shop_name = str(response_data['shop_name'])
#         cust_obj.person_name = 
        return{
                'responseCode': 503,
                'Message': "Order " + str(order_obj.id) + " Successfully Edited"
            }
    except ObjectDoesNotExist:
        return{
                'responseCode': 503,
                'Message': "Order does not exist"
            }
        