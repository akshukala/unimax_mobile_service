from mobileservice.utils.resource import Resource
class Ping(Resource):

    def get(self):
        """
           This method is used to test service
        """

        return {"success": True}
    get.authenticated = False
