import urllib


from django.shortcuts import render_to_response
from django.http import, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext


# Create your views here.

def index(request,
          template_name="index.html"):

    # projects = Project.objects.all()
    return render_to_response(template_name,
        {},
        context_instance=RequestContext(request))



