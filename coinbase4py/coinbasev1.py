import urllib2
import json
import hashlib
import hmac
import time

from django.conf import settings

# GET /api/v1/account/balance HTTP/1.1
# Accept: */*
# User-Agent: Python
# ACCESS_KEY: <YOUR-API-KEY>
# ACCESS_SIGNATURE: <YOUR-COMPUTED-SIGNATURE>
# ACCESS_NONCE: <YOUR-UPDATED-NONCE>
# Connection: close
# Host: coinbase.com
class CoinbaseV1():

    def refresh_token(
            self,
            access_token,
            refresh_token,
            app_client_id,
            app_client_secret):

        opener = urllib2.build_opener()
        refresh_body = {
            'grant_type':'refresh_token',
            'access_token':access_token,
            'refresh_token':refresh_token,
            'client_id':app_client_id,
            'client_secret':app_client_secret
        }

        # if settings.DEBUG == 'true':
        #     print json.dumps(refresh_body)

        refresh_response = opener.open(urllib2.Request(
            'https://coinbase.com/oauth/token?access_token={0}'.format(access_token),
            json.dumps(refresh_body),
            {'Content-Type': 'application/json'}))

        response_string = refresh_response.read()

        return json.loads(response_string)

    # this version is used for no oauth or api requests
    def get_and_post_http(
            self,
            url,
            body=None):

        opener = urllib2.build_opener()

        try:
            if body:
                print 'POST body: {0}'.format(body)

            response_stream = opener.open(urllib2.Request('{0}'.format(url),body,{'Content-Type': 'application/json'}))

            #return the valid access token, this will be updated if needed to be refreshed
            response_string = response_stream.read()
            response_object = json.loads(response_string)
            response_object['error_code'] = None

            return response_object

        except urllib2.HTTPError as e:
            return {'error_code':e.code,'message':'HTTP Error'}

    # this really neads to be refactored to always return an object
    # so that the client refresh can have control over the model.
    # the behvior here is to act as a post when a body is present and get when None
    def get_and_post_http_oauth(
            self,
            url,
            access_token,
            refresh_token,
            body=None):

        opener = urllib2.build_opener()

        try:
            print 'url: {0}?access_token={1}'.format(url,access_token)
            if body:
                print 'POST body: {0}'.format(body)

            response_stream = opener.open(urllib2.Request('{0}?access_token={1}'.format(url,access_token),body,{'Content-Type': 'application/json'}))

            #return the valid access token, this will be updated if needed to be refreshed
            response_string = response_stream.read()
            response_object = json.loads(response_string)
            response_object['access_token'] = access_token
            response_object['refresh_token'] = refresh_token
            response_object['error_code'] = None

            return response_object

        except urllib2.HTTPError as e:
            return {'error_code':e.code,'message':'HTTP Error'}


    def get_and_post_http_api(
            self,
            url,
            body=None,
            access_key=None,
            access_secret=None):

        opener = urllib2.build_opener()
        nonce = int(time.time() * 1e6)
        message = str(nonce) + url + ('' if body is None else body)
        signature = hmac.new(access_secret, message, hashlib.sha256).hexdigest()
        opener.addheaders = [('ACCESS_KEY', access_key),
                             ('ACCESS_SIGNATURE', signature),
                             ('ACCESS_NONCE', nonce)]
        try:
            response = opener.open(urllib2.Request(url,body,{'Content-Type': 'application/json'}))
            return response
        except urllib2.HTTPError as e:
            return e

    def get_json_api(self, url,
                 body,
                 access_key,
                 access_secret):
        response = self.get_http(url,body,access_key,access_secret)
        json_response = response.read()
        return json.loads(json_response)

    def post_json_api(self, url, data_obj,
                 access_key,
                 access_secret):
        response = self.get_http(url,json.dumps(data_obj),access_key,access_secret)
        json_response = response.read()
        return json.loads(json_response)

# Redirect the user to this page
# https://coinbase.com/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_CALLBACK_URL
    def get_oauth_redirect(self, client_id, client_callback):

        return 'https://coinbase.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}'.format(
            client_id,
            client_callback)

# Initiate a POST request to get the access token
# https://coinbase.com/oauth/token?grant_type=authorization_code&code=CODE&redirect_uri=YOUR_CALLBACK_URL&client_id=CLIENT_ID&client_secret=CLIENT_SECRET
    def post_oauth_response(self, code, client_callback, client_id, client_secret):
        post_url = 'https://coinbase.com/oauth/token?grant_type=authorization_code' \
                   '&code={0}&' \
                   'redirect_uri={1}&' \
                   'client_id={2}' \
                   '&client_secret={3}'.format(
            code,
            client_callback,
            client_id,
            client_secret
        )

        oauth_response = self.get_and_post_http(post_url, {})

        # Response containing the 'access_token'
        # {
        #     "access_token": "...",
        #     "refresh_token": "...",
        #     "token_type": "bearer",
        #     "expire_in": 7200,
        #     "scope": "universal"
        # }

        return oauth_response



    def make_button(self,
                    button_request,
                    access_token,
                    refresh_token,
                    client_id,
                    client_secret):

        #refres the token
        refresh_response = self.refresh_token(
            access_token,
            refresh_token,
            client_id,
            client_secret)

        #this has a body so it will POST
        # use the new token
        button_response = self.get_and_post_http_oauth('https://coinbase.com/api/v1/buttons',
                                       refresh_response['access_token'],
                                       refresh_response['refresh_token'],
                                       json.dumps(button_request))

        button_response['access_token'] = refresh_response['access_token']
        button_response['refresh_token'] = refresh_response['refresh_token']


        return button_response

# # Request
# GET https://api.coinbase.com/v1/users
#
# # Response
# {
#   "users": [
#     {
#       "user": {
#         "id": "512db383f8182bd24d000001",
#         "name": "User One",
#         "email": "user1@example.com",
#         "time_zone": "Pacific Time (US & Canada)",
#         "native_currency": "USD",
#         "balance": {
#           "amount": "49.76000000",
#           "currency": "BTC"
#         },
#         "merchant": {
#           "company_name": "Company Name, Inc.",
#           "logo": {
#             "small": "http://smalllogo.example",
#             "medium": "http://mediumlogo.example",
#             "url": "http://logo.example"
#           }
#         },
#         "buy_level": 1,
#         "sell_level": 1,
#         "buy_limit": {
#           "amount": "10.00000000",
#           "currency": "BTC"
#         },
#         "sell_limit": {
#           "amount": "100.00000000",
#           "currency": "BTC"
#         }
#       }
#     }
#   ]
# }
    def get_oauth_users(self,
                        access_token,
                        refresh_token,
                        client_id,
                        client_secret):

        #refres the token
        refresh_response = self.refresh_token(
            access_token,
            refresh_token,
            client_id,
            client_secret)

        #this has a no body so it will GET
        response_object = self.get_and_post_http_oauth(
            'https://api.coinbase.com/v1/users',
            refresh_response['access_token'],
            refresh_response['refresh_token'])

        response_object['access_token'] = refresh_response['access_token']
        response_object['refresh_token'] = refresh_response['refresh_token']

        return response_object

