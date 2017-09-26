import os
import time
from flask import current_app as app
from flask import Flask, redirect
from flask.globals import request
from flask_restful import Resource
from werkzeug import secure_filename
from __builtin__ import file


class Cust_Image(Resource):

    def post(self):
        print "Hello"
        file = request.files['file']
        print file
        return "Success"