from django.core.exceptions import ObjectDoesNotExist
from flask import current_app as app

from uni_db.mob_app.models import CustOrder, Order_Item, Customer
from mobileservice.utils.auth import get_user


def handle_request(response_data):
    print response_data
    try:
        order_obj = CustOrder.objects.get(id=int(response_data['order_id']))
        cust_obj = order_obj.owner
        cust_obj.shop_name = str(response_data['shop_name'])
        cust_obj.person_name = str(response_data['cust_name'])
        cust_obj.contact_no = str(response_data['contact'])
        cust_obj.area = str(response_data['area'])
        if response_data['addr']:
            cust_obj.address = str(response_data['addr'])
        if response_data['gst']:
            cust_obj.gst_no = str(response_data['gst'])
        if response_data['pan']:
            cust_obj.pan_no = str(response_data['pan'])
        cust_obj.save()

        order = CustOrder.objects.create(owner=order_obj.owner,
                                         payment_type=int(response_data['pay_type']),
                                         created_on=order_obj.created_on,
                                         created_by=order_obj.created_by,
                                         modified_by=str(get_user().username),
                                         grand_total=float(response_data['total']))
        if response_data['remark']:
            order_obj.remarks = str(response_data['remark'])
        order_obj.save()

        items = str(response_data['itemname']).split('$')
        qty = (response_data['qty']).split('$')
        price = (response_data['item_price']).split("$")
        for itr in range(0, len(items)-1):
            print qty[itr]
            if int(qty[itr])==0:
                continue
            else:
                temp = float(price[itr])/int(qty[itr])
                Order_Item.objects.create(order=order, item_name=items[itr],
                                      quantity=int(qty[itr]),
                                      selling_price=temp,
                                      total_price=float(price[itr]))
        order_obj.status = "CANCELLED"
        order_obj.save()
        return{
                'responseCode': 200,
                'Message': "Order Successfully Edited"
            }
    except ObjectDoesNotExist:
        return{
                'responseCode': 503,
                'Message': "Order does not exist"
            }