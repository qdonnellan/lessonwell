from tests.main_test_handler import TestBase
from controllers.stripe_controllers.new_customer import new_customer
import stripe
from stripe_keys import api_key
import unittest

@unittest.skip('skipping long stripe tests, should activate(#) on/off as needed')
class StripeNewCustomerTest(TestBase):
    '''
    test the implementation of the stripe customer creation process
    '''
    def generate_sample_token(self, card='4242424242424242', cvc='123', MM=12, YYYY=2015):
        '''
        generate a sample token for test purposes
        '''
        stripe.api_key = api_key
        return stripe.Token.create(card={"number": card, "exp_month": MM, "exp_year": YYYY, "cvc": cvc })

    def test_new_customer_with_valid_card(self):
        '''
        a new customer with a valid card should be created on stripe with a successfuly response
        '''
        stripeToken = self.generate_sample_token()
        user = self.create_and_return_local_user()
        self.assertIsNone(user.stripeID) #should have no stripe ID before   
        self.assertTrue(new_customer(stripeToken, "user@example.com", user))
        self.assertIn('cus_', user.stripeID) #should have a stripe ID afterwards

    def test_new_customer_with_invalid_card(self):
        '''
        a new customer with an invalid card should be rejected by stripe

        card# 4000000000000127 is designed by the people at Stripe to throw an invalid card error (cvc error)
        '''
        stripeToken = self.generate_sample_token(card='4000000000000127')
        user = self.create_and_return_local_user()
        self.assertIsNone(user.stripeID)
        self.assertRaises(Exception, new_customer, stripeToken, 'user@example.com', user)
        self.assertIsNone(user.stripeID) #no stripe ID should be created for this user

    def test_new_customer_with_none_user(self):
        '''
        a new customer call without passing a user should not trigger a stripe customer creation
        '''
        self.assertFalse(new_customer(stripeToken='', email='user@example.com', user=None))
