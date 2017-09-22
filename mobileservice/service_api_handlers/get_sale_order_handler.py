from datetime import datetime

from uni_db.mob_app.models import CustOrder, Order_Item


def create_response(orders):
    response = []
    for order in orders:
        order_dict = {}
        order_dict['order_id'] = str(order.id)
        order_dict['created_on'] = order.created_on.strftime("%d/%m/%Y")
        order_dict['shop_name'] = str(order.owner.shop_name)
        order_dict['area'] = str(order.owner.area)
        order_item_list = []
        for oi in Order_Item.objects.filter(order=order):
            temp = ""
            temp += str(oi.item_name) + " - " + str(oi.quantity)
            order_item_list.append(temp)
        order_dict['item_list'] = order_item_list
        order_dict['total'] = (order.grand_total)
        response.append(order_dict)
    return response


def handle_request(response_data):
    print response_data
    if int(response_data['type']) == 1:
        '''Get todays orders'''
        today = datetime.now().date()
        orders = CustOrder.objects.filter(created_on__contains=today)
        return create_response(orders)
    elif int(response_data['type'] == 2):
        '''Get orders by date range'''
        return "Success"
    else:
        '''get all orders'''
        return "Success"