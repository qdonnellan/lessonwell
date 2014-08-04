from controllers.stripe_controllers.redeem import verify_code, redeem_code
from flask.ext.restful import Resource, reqparse
from controllers.fetch_user import get_active_user
import logging

class RedeemAPI(Resource):
    """
    api handlers for customer objects
    """

    def post(self):
        """
        attempt to redeem a coupon code; if none exists, return an error
        """
        parser = reqparse.RequestParser()
        parser.add_argument('sponsor_code', type=str)
        args = parser.parse_args()
        sponsor_code = args['sponsor_code']

        success = False

        if verify_code(sponsor_code):
            teacher = get_active_user()
            if teacher:
                try:
                    redeem_code(
                        teacher = teacher, 
                        coupon_code = sponsor_code
                    )
                except Exception as e:
                    logging.info(e)
                else:
                    success = True

        if success:
            return {'success' : True}
        else:
            return {'success' : False}
            
