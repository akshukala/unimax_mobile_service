from flask.globals import request
from flask_restful import Resource
from uni_db.mob_app.models import FirebaseToken


class Token(Resource):
    def post(self):
        request_data = request.get_json(force=True)
        FirebaseToken.objects.get_or_create(token_id=str(request_data.get('token')))
        return{
                    'responseCode': 200,
                    'Message': "Firebase token added Successfully"
                }