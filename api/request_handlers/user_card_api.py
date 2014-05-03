from main_api_handler import APIHandler
from controllers.stripe_controllers.get_user_card import get_user_card
from controllers.stripe_controllers.change_card import change_card
from decorators.auth import local_user_required
import logging

class UserCardAPI(APIHandler):
    """
    handle all get/post requests for the user_card api
    """

    @local_user_required
    def get(self):
        """
        handle the get request for the user_card api
        """
        try:
            data = get_user_card()

        except Exception as e:
            data = {'error' : str(e)}

        self.write_json(data)

    @local_user_required
    def post(self):
        """
        change the card on file
        """
        try:
            card_info = self.request.POST.get('stripeToken')
            change_card(card_info)
            self.redirect('/edit')
        except:
            self.write_json({'error' : 'there was an error processing your request'})
