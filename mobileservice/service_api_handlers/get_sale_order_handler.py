from datetime import datetime, timedelta

from uni_db.mob_app.models import (CustOrder, Order_Item,
                                   User_Details, Shop_Images)
from mobileservice.utils.auth import get_user


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
        order_dict['created_by'] = str(order.owner.created_by.first_name) + " " + str(order.owner.created_by.last_name)
        order_item_list = []
        qty_list = []
        for oi in Order_Item.objects.filter(order=order):
            order_item_list.append(str(oi.item_name))
            qty_list.append(oi.quantity)
        if "1/2 inch" in order_item_list:
            index = order_item_list.index("1/2 inch")
            order_dict['1/2 inch'] = qty_list[index]
        else:
            order_dict['1/2 inch'] = 0
        if "3/4 inch" in order_item_list:
            index = order_item_list.index("3/4 inch")
            order_dict['3/4 inch'] = qty_list[index]
        else:
            order_dict['3/4 inch'] = 0
        if "1 inch" in order_item_list:
            index = order_item_list.index("1 inch")
            order_dict['1 inch'] = qty_list[index]
        else:
            order_dict['1 inch'] = 0
        order_dict['total'] = (order.grand_total)
        image_str = ''
        img_obj = Shop_Images.objects.filter(customer=order.owner)
        if len(img_obj) >=3:
            order_dict['img_one'] = str(img_obj[0].img_url)
            order_dict['img_two'] = str(img_obj[1].img_url)
            order_dict['img_three'] = str(img_obj[2].img_url)
        elif len(img_obj) ==2:
            order_dict['img_one'] = str(img_obj[0].img_url)
            order_dict['img_two'] = str(img_obj[1].img_url)
            order_dict['img_three'] = ''
        elif len(img_obj) ==1:
            order_dict['img_one'] = str(img_obj[0].img_url)
            order_dict['img_two'] = ''
            order_dict['img_three'] = ''
        else:
            order_dict['img_one'] = ''
            order_dict['img_two'] = ''
            order_dict['img_three'] = ''
        # for img in Shop_Images.objects.filter(customer=order.owner):
        #     image_str += str(img.img_url) + ";"
        # order_dict['img_urls'] = image_str
        response.append(order_dict)
    return response


def handle_request(response_data):
    user_obj = User_Details.objects.get(user=get_user())
    if int(response_data['type']) == 1:
        '''Get todays orders'''
        #today = datetime.now().date()
        if user_obj.is_admin:
            orders = CustOrder.objects.filter(is_active=True
                                              ).exclude(status='CANCELLED')[::-1]
        else:
            orders = CustOrder.objects.filter(is_active=True,
                                              created_by=str(get_user().username)
                                              ).exclude(status='CANCELLED')[::-1]
        return{
                'responseCode': 200,
                'response_data': create_response(orders)
            }
    elif int(response_data['type']) == 2:
        '''Get orders by date range'''
        start_date = datetime.strptime(str(response_data['start_date'])+' 0:0:0','%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(str(response_data['end_date'])+' 0:0:0', '%Y-%m-%d %H:%M:%S')
        new_end = end_date + timedelta(days=1)
        if user_obj.is_admin:
            orders = CustOrder.objects.filter(created_on__gte=start_date,
                                              created_on__lte=new_end,
                                              is_active=True).exclude(status='CANCELLED')[::-1]
        else:
            orders = CustOrder.objects.filter(created_on__gte=start_date,
                                              created_on__lte=new_end,
                                              created_by=str(get_user().username),
                                              is_active=True).exclude(status='CANCELLED')[::-1]
        return{
                'responseCode': 200,
                'response_data': create_response(orders)
            }
    else:
        '''get all orders'''
        if user_obj.is_admin:
            orders = CustOrder.objects.filter(is_active=True
                                              ).exclude(status='CANCELLED')[::-1]
        else:
            orders = CustOrder.objects.filter(is_active=True,
                                              created_by=str(get_user().username)
                                              ).exclude(status='CANCELLED')[::-1]
        return{
                'responseCode': 200,
                'response_data': create_response(orders)
            }
