from datetime import datetime

from uni_db.mob_app.models import CustOrder, Order_Item


def create_response(orders):
    response = []
    for order in orders:
        order_dict = {}
        order_dict['order_id'] = str(order.id)
        order_dict['created_on'] = order.created_on.strftime("%d/%m/%Y")
        order_dict['shop_name'] = str(order.owner.shop_name)
        order_dict['cust_name'] = str(order.owner.person_name)
        order_dict['contact'] = str(order.owner.contact_no)
        order_dict['addr'] = str(order.owner.address)
        order_dict['area'] = str(order.owner.area)
        order_dict['gst'] = str(order.owner.gst_no)
        order_dict['pan'] = str(order.owner.pan_no)
        order_dict['remark'] = str(order.remarks)
        order_dict['pay_type'] = str(order.payment_type)
        order_item_list = ""
        qty_list = ""
        selling_price_list = ""
        item_price_list = ""
        for oi in Order_Item.objects.filter(order=order):
            order_item_list += str(oi.item_name) + ":"
            qty_list += str(oi.quantity) + ":"
            selling_price_list += str(oi.selling_price) + ":"
            item_price_list += str(oi.total_price) + ":"
        order_dict['item_list'] = order_item_list
        order_dict['qty'] = qty_list
        order_dict['sp_list'] = selling_price_list
        order_dict['item_price_list'] = item_price_list
        order_dict['total'] = (order.grand_total)
        response.append(order_dict)
    return response


def handle_request(response_data):
    if int(response_data['type']) == 1:
        '''Get todays orders'''
        today = datetime.now().date()
        orders = CustOrder.objects.filter(created_on__contains=today)[::-1]
        return{
                'responseCode': 200,
                'response_data': create_response(orders)
            }
    elif int(response_data['type'] == 2):
        '''Get orders by date range'''
        start_date = datetime.strptime(str(response_data['start_date'])+' 0:0:0','%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(str(response_data['end_date'])+' 0:0:0', '%Y-%m-%d %H:%M:%S')
        orders = CustOrder.objects.filter(created_on__range=[start_date, end_date])
        return{
                'responseCode': 200,
                'response_data': create_response(orders)
            }
    else:
        '''get all orders'''
        orders = CustOrder.objects.all()[::-1]
        return{
                'responseCode': 200,
                'response_data': create_response(orders)
            }
