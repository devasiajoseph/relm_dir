from django import forms
from django.conf import settings
from app.utilities import reply_object
from app.models import SellerRequest
from app.utilities import create_key, send_seller_approval_email


class ApproveSellerRequestForm(forms.Form):
    seller_request_id = forms.IntegerField()
    decision = forms.CharField()

    def save_decision(self):
        response = reply_object()
        #try:
        if True:
            seller_request = SellerRequest.objects.get(
                pk=self.cleaned_data["seller_request_id"])
            if self.cleaned_data["decision"] == settings.\
                    SELLER_REQUEST_STATUS["APPROVED"]:
                key_object = create_key(seller_request.email, 2)
                seller_request.approval_key = key_object["key"]
                seller_request.key_expires = key_object["expiry"]
                seller_request.status = settings.SELLER_REQUEST_STATUS[
                    "APPROVED"]
                seller_request.save()
                response["request_status"] = settings.SELLER_REQUEST_STATUS[
                    "APPROVED"]
                response["code"] = settings.APP_CODE["CALLBACK"]
                send_seller_approval_email(seller_request.email, key_object["key"])
            elif self.cleaned_data["decision"] == settings.\
                    SELLER_REQUEST_STATUS["REJECTED"]:
                seller_request.status = settings.SELLER_REQUEST_STATUS[
                    "REJECTED"]
                seller_request.save()
                response["request_status"] = settings.SELLER_REQUEST_STATUS[
                    "REJECTED"]
                response["code"] = settings.APP_CODE["CALLBACK"]
            else:
                response["code"] = settings.APP_CODE["INVALID REQUEST"]

        #except:
        #    response["code"] = settings.APP_CODE["SYSTEM ERROR"]

        return response
