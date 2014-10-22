from django.db import models
from django.contrib.auth.models import User

import re

reply_re = re.compile("^@(\w+)")

# USER
# username
# password
# email
# first_name
# last_name
class CoinbaseUser(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=250, unique=False, blank=True,  null=True)
    coinbase_access_token = models.CharField(max_length=250, unique=False, blank=True,  null=True)
    coinbase_refresh_token = models.CharField(max_length=250, unique=False, blank=True,  null=True)
    coinbase_callback_secret = models.CharField(max_length=128, unique=False, blank=True,  null=True)

    class Meta:
        app_label = "webapp"

    def __unicode__(self):
        return self.user.username

class CoinbaseButton(models.Model):
    code = models.CharField(max_length=64)
    external_id = models.TextField()
    button_response = models.TextField()
    type = models.CharField(max_length=16,null=True,blank=True)
    button_guid = models.CharField(max_length=128,null=True,blank=True)
    owner = models.ForeignKey('CoinbaseUser',null=True,blank=True)
    callback_url = models.CharField(max_length=256,null=True,blank=True)
    total_coin_cents = models.BigIntegerField(default=0,null=True,blank=True)
    total_coin_currency_iso = models.CharField(max_length=3,null=True,blank=True)
    enabled = models.NullBooleanField(default=False, null=True)

    class Meta:
        app_label = "webapp"

    def __unicode__(self):
        return self.code