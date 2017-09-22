from django.core.exceptions import ObjectDoesNotExist
from flask import current_app as app

from uni_db.mob_app.models import CustOrder, Order_Item, Customer
from mobileservice.utils.auth import get_user
import code


def handle_request(code):
    print code
    return "Success"