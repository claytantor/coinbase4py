import unittest
import uuid
import json

from django.conf import settings

from coinbase4py.coinbasev1 import CoinbaseV1

#this test is to verify that buttons are created for the API oath owner
class CoinbaseV1ClientCreateButtonsTestCase(unittest.TestCase):
    def test_button1(self):

        #make the guid
        button_guid = str(uuid.uuid1())

        #get state
        test_state = TestState()
        state_model = test_state.getUser(settings.USER_ONE)

        button_request = {
            'button':{
                'name':'test button {0}'.format(button_guid),
                'custom':button_guid,
                'description':'test button {0}'.format(button_guid),
                'price_string':1.00,
                'price_currency_iso':'USD',
                'button_type':'donation',
                'style':'donation_small',
                'choose_price':True,
                'price1':5.00,
                'price2':10.00,
                'price3':25.00,
                'price4':100.00
            }
        }

        coinbase_client = CoinbaseV1()

        refresh_response = coinbase_client.refresh_token(
            state_model['refresh_token'],
            settings.COINBASE_OAUTH_CLIENT_ID,
            settings.COINBASE_OAUTH_CLIENT_SECRET)

        #we have to do this to simulate a refresh
        state_model['refresh_token'] = refresh_response['refresh_token']
        state_model['access_token'] = refresh_response['access_token']

        test_state.saveUser(settings.USER_ONE,state_model)

        button_response = coinbase_client.post_button_oauth(
                button_request,
                refresh_response['access_token'],
                refresh_response['refresh_token'],
                settings.COINBASE_OAUTH_CLIENT_ID,
                settings.COINBASE_OAUTH_CLIENT_SECRET)

        #we have to do this to simulate a refresh
        state_model['refresh_token'] = button_response['refresh_token']
        state_model['access_token'] = button_response['access_token']
        test_state.saveUser(settings.USER_ONE,state_model)

        assert True


    def test_button2(self):

        #make the guid
        button_guid = str(uuid.uuid1())

        #get state
        test_state = TestState()
        state_model = test_state.getUser(settings.USER_TWO)

        button_request = {
            'button':{
                'name':'test button {0}'.format(button_guid),
                'custom':button_guid,
                'description':'test button {0}'.format(button_guid),
                'price_string':1.00,
                'price_currency_iso':'BTC',
                'button_type':'buy_now',
                'style':'buy_now_small',
                'choose_price':False
            }
        }

        coinbase_client = CoinbaseV1()

        refresh_response = coinbase_client.refresh_token(
            state_model['refresh_token'],
            settings.COINBASE_OAUTH_CLIENT_ID,
            settings.COINBASE_OAUTH_CLIENT_SECRET)

        #we have to do this to simulate a refresh
        state_model['refresh_token'] = refresh_response['refresh_token']
        state_model['access_token'] = refresh_response['access_token']
        test_state.saveUser(settings.USER_TWO,state_model)

        button_response = coinbase_client.post_button_oauth(
                button_request,
                refresh_response['access_token'],
                refresh_response['refresh_token'],
                settings.COINBASE_OAUTH_CLIENT_ID,
                settings.COINBASE_OAUTH_CLIENT_SECRET)

        #we have to do this to simulate a refresh
        state_model['refresh_token'] = button_response['refresh_token']
        state_model['access_token'] = button_response['access_token']
        test_state.saveUser(settings.USER_ONE,state_model)

        assert True

#simulates a db
class TestState():
    def getUser(self,username):
        f = open('{0}/{1}.json'.format(settings.TEST_STATE_DIR,username), 'r')
        state_model = json.loads(f.read())
        f.close()
        return state_model

    def saveUser(self,username, state):
        f = open('{0}/{1}.json'.format(settings.TEST_STATE_DIR,username), 'w')
        f.write(json.dumps(state))
        f.close()


if __name__ == '__main__':
    unittest.main()