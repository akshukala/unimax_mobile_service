from flask_restful import Resource
import requests
import json
from uni_db.mob_app.models import FirebaseToken


class Send_Notification(Resource):

    def get(self):

        title = "hello"
        desc = "Welcome to Unimax"
        token_list = [str(obj.token_id) for obj in FirebaseToken.objects.all()]
        API_ACCESS_KEY = 'AIzaSyCoFp3hp-ypjISBbn3ms96dCq4aYFkuWTY'
        registrationIds = token_list
        url = 'https://android.googleapis.com/gcm/send'
        fields = {
            'registration_ids': registrationIds,
            "data": {
              "name": "Unimax",
              "body": desc,
              "title": title
            }
        }

        # Adding empty header as parameters are being sent in payload
        headers = {'Authorization': 'key=' + API_ACCESS_KEY,
                   'Content-Type': 'application/json'}
        result = requests.post(url, data=json.dumps(fields), headers=headers)
        print(result)
        return{
                    'responseCode': 200,
                    'response': "sss"
                }