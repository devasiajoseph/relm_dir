from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from app.utilities import reply_object, create_key
import simplejson
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
import datetime
from app.models import SellerRequest


def seller_request_list(request, list_type, page):
    if list_type == "all":
        request_list = SellerRequest.objects.all()
    else:
        request_list = SellerRequest.objects.filter(status=list_type)
    label_map = {"pending": "warning",
                 "approved": "success",
                 "rejected": "important"}
    return render_to_response(
        "seller_request_list.html",
        context_instance=RequestContext(request,
                                        {"list_type": list_type,
                                         "request_list": request_list,
                                         "label_map": label_map}))
