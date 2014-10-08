from django.db import models
from django.contrib.auth.models import User

import re

reply_re = re.compile("^@(\w+)")

class CoinbaseUser(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=250, unique=False, blank=True,  null=True)
    coinbase_access_token = models.CharField(max_length=250, unique=False, blank=True,  null=True)
    coinbase_refresh_token = models.CharField(max_length=250, unique=False, blank=True,  null=True)
    coinbase_callback_secret = models.CharField(max_length=128, unique=False, blank=True,  null=True)

    def __unicode__(self):
        return self.user.username
