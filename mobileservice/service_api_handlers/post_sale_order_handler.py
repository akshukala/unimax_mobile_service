from flask import current_app as app

from uni_db.mob_app.models import CustOrder, Order_Item, Customer
from mobileservice.utils.auth import get_user


def handle_request(request_data):
    try:
        cust_obj = Customer.objects.create(shop_name=str(request_data['cust_name']),
                                           person_name=str(request_data['shop_name']),
                                           contact_no=str(request_data['contact']),
                                           area=str(request_data['area']),
                                           created_by=get_user(),
                                           modified_by=get_user())
        if request_data['addr']:
            cust_obj.address = str(request_data['addr'])
        if request_data['gst']:
            cust_obj.gst_no = str(request_data['gst'])
        if request_data['pan']:
            cust_obj.pan_no = str(request_data['pan'])
        cust_obj.save()

        order_obj = CustOrder.objects.create(owner=cust_obj,
                                             payment_type=int(request_data['pay_type']),
                                             created_by=str(get_user().username),
                                             modified_by=str(get_user().username),
                                             grand_total=float(request_data['total']))
        if request_data['remark']:
            order_obj.remarks = str(request_data['remark'])
        order_obj.save()

        items = str(request_data['itemname']).split('$')
        qty = str(request_data['qty']).split('$')
        sp = str(request_data['sp']).split('$')
        for itr in range(0, len(items)-1):
            Order_Item.objects.create(order=order_obj, item_name=items[itr],
                                      quantity=qty[itr], selling_price=sp[itr],
                                      total_price=(float(qty[itr]) * float(sp[itr])))
        return {
                'responseCode': 200,
                'Message': "Order saved",
                'order_id': str(order_obj.id)
            }
    except Exception as e:
            app.logger.debug(str(e))
            return {'responseCode': 500,
                    'Message': "Order not saved"}