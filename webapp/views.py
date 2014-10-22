import json
import uuid

from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from coinbase4py.coinbasev1 import CoinbaseV1

from webapp.models import CoinbaseUser,CoinbaseButton
from webapp.forms import ButtonForm


# Create your views here.

def index(request,
          template_name="index.html"):

    # projects = Project.objects.all()
    return render_to_response(template_name,
        {},
        context_instance=RequestContext(request))

@login_required(login_url='/login.html')
def home(request,
          template_name="home.html"):


    #get the user
    cbuser = CoinbaseUser.objects.get(user=request.user)
    user_buttons = CoinbaseButton.objects.filter(owner=cbuser)
    context = {"user_buttons":user_buttons}

    #create the client instance
    client_coinbase = CoinbaseV1()

    #get the user object using the access token
    cbuser_response = client_coinbase.get_oauth_users(
        cbuser.coinbase_access_token,
        cbuser.coinbase_refresh_token,
        settings.COINBASE_OAUTH_CLIENT_ID,
        settings.COINBASE_OAUTH_CLIENT_SECRET)

    oauth_user = cbuser_response['users'][0]['user']
    context['coinbase_user_json'] = \
        json.dumps(oauth_user, sort_keys=True, indent=4, separators=(',', ': '))


    if request.method == 'GET':
        button_form = ButtonForm()
        context['button_form'] = button_form
    elif request.method == 'POST':
        button_form = ButtonForm(request.POST)
        context['button_form'] = button_form
        if button_form.is_valid():
            #make a button id that will persist for callback
            button_guuid = str(uuid.uuid1())

            # when the button is paid a callback to the application
            # will be made with the transaction details
            callback_url = '{0}/{1}/?secret={2}'.format(
                settings.COINBASE_ORDER_CALLBACK,
                cbuser.user.username,
                cbuser.coinbase_callback_secret)

            button_request = {
                'button':{
                    'name':'{0} {1}'.format(str(button_form.cleaned_data['payment_type']), button_guuid ),
                    'custom':button_guuid,
                    'description':str(button_form.cleaned_data['description']),
                    'price_string':button_form.cleaned_data['amount'],
                    'price_currency_iso':'BTC',
                    'button_type':str(button_form.cleaned_data['payment_type']),
                    'callback_url':callback_url
                }
            }

            button_response = client_coinbase.make_button(
                    button_request,
                    cbuser.coinbase_access_token,
                    cbuser.coinbase_refresh_token,
                    settings.COINBASE_OAUTH_CLIENT_ID,
                    settings.COINBASE_OAUTH_CLIENT_SECRET)

            #now save the refresh token from the unit call
            cbuser.coinbase_refresh_token = button_response['refresh_token']
            cbuser.coinbase_access_token = button_response['access_token']
            cbuser.save()

            if button_response['error_code']:
                return render_to_response('error.html',
                    {'error':'{0}\n{1}'.format(
                        json.dumps(button_request),
                        json.dumps(button_response),
                    )},
                    context_instance=RequestContext(request))
            else:
                #add the created buttons
                button_created = CoinbaseButton.objects.create(
                    code=button_response['button']['code'],
                    external_id=button_guuid,
                    button_response=json.dumps(button_response),
                    button_guid=button_guuid,
                    callback_url=callback_url,
                    type=str(button_form.cleaned_data['payment_type']),
                    owner=cbuser,
                    enabled=True)


    return render_to_response(template_name,
        context,
        context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('{0}/index.html'.format(settings.COINBASE4PY_APP_URL))

def login_user(request):

    coinbase_client = CoinbaseV1()

    # we need to get the the OAUth redirect url, this will sent the user to coinbase
    # once they authorize the application coinbase will send the browser to the URL
    # set to settings.COINBASE_OAUTH_CLIENT_CALLBACK
    redirect = coinbase_client.get_oauth_redirect(
            settings.COINBASE_OAUTH_CLIENT_ID,
            settings.COINBASE_OAUTH_CLIENT_CALLBACK)

    return HttpResponseRedirect(redirect)

def cb_auth_redirect(request, template_name="home.html"):
    context = {}

    if request.method == 'GET':
        #use the code to get an access token

        #use the code to POST and get an access_token
        coinbase_client = CoinbaseV1()

        #def get_oauth_response(self, code, client_callback, client_id, client_secret):
        response_obj = coinbase_client.post_oauth_response(
            request.GET['code'],
            settings.COINBASE_OAUTH_CLIENT_CALLBACK,
            settings.COINBASE_OAUTH_CLIENT_ID,
            settings.COINBASE_OAUTH_CLIENT_SECRET)

        print '=== before user call: {0}'.format(json.dumps(response_obj))

        #get the user object using the access token
        cbuser_response = coinbase_client.get_oauth_users(
            response_obj['access_token'],
            response_obj['refresh_token'],
            settings.COINBASE_OAUTH_CLIENT_ID,
            settings.COINBASE_OAUTH_CLIENT_SECRET)

        print '=== after user call: {0}'.format(json.dumps(cbuser_response))

        oauth_user = cbuser_response['users'][0]['user']

        # try to find the user if it doesnt exist then make it,
        # otherwise update it

        cbuser = None

        try:
            cbuser = CoinbaseUser.objects.get(user__email=oauth_user['email'])
            cbuser.coinbase_refresh_token = cbuser_response['refresh_token']
            cbuser.coinbase_access_token = cbuser_response['access_token']
            cbuser.save()

        except ObjectDoesNotExist:

            # every user has the same passowrd, thats because passwords dont matter
            # when you have oauth, want an extra level of security? build a password
            # workflow.
            # create_user(self, username, email=None, password=None, **extra_fields):
            user = User.objects.create_user(
                        oauth_user['email'],
                        oauth_user['email'],
                        settings.COINBASE4PY_PW_SECRET_KEY)

            # user = models.ForeignKey(User)
            # name = models.CharField(max_length=250, unique=False, blank=True,  null=True)
            # coinbase_access_token = models.CharField(max_length=250, unique=False, blank=True,  null=True)
            # coinbase_refresh_token = models.CharField(max_length=250, unique=False, blank=True,  null=True)
            # coinbase_callback_secret = models.CharField(max_length=128, unique=False, blank=True,  null=True)
            cbuser = CoinbaseUser.objects.create(
                user=user,
                name=oauth_user['name'],
                coinbase_access_token=response_obj['access_token'],
                coinbase_refresh_token=response_obj['refresh_token'],
                coinbase_callback_secret=settings.COINBASE4PY_PW_SECRET_KEY
            )

        if cbuser:
            auth_user = authenticate(username=oauth_user['email'], password=settings.COINBASE4PY_PW_SECRET_KEY)
            if auth_user is not None:
                if auth_user.is_active:
                    login(request, auth_user)
                    # Redirect to a success page.
                    #needs the full app url for redirect
                    return HttpResponseRedirect('{0}/home.html'.format(settings.COINBASE4PY_APP_URL))
                else:
                    # # Return a 'disabled account' error message
                    # context['message']=request.POST['username']+' account has been suspended.'
                    return render_to_response('error.html',{'message':'auth user is not empty but us unactive'},context_instance=RequestContext(request))
            else:
                return render_to_response('error.html',{'message':'auth user is empty or (most likely) the GITPATRON_PW_SECRET_KEY is incorrect '},context_instance=RequestContext(request))


        #use the new user to make the home page
        context['cbuser'] = cbuser


    return render_to_response(template_name,
        context,
        context_instance=RequestContext(request))



@require_http_methods(["POST"])
@csrf_exempt
def cbcallback(request,button_owner_username):
    data = {}
    return HttpResponse(json.dumps(data), mimetype='application/json')
