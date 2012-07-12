"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""

from django.test import TestCase
from app.tests import logged_in_client, verify_json_response
from app.models import SellerRequest
from django.conf import settings
import simplejson


class TestSeller(TestCase):
    fixtures = ['test_data.json']

    def test_seller_approval(self):
        """
        Atleast one pending accounts needed for this test
        """
        c = logged_in_client()
        seller_request = SellerRequest.objects.filter(
            status=settings.SELLER_REQUEST_STATUS["PENDING"])[0]
        approval = {"decision": settings.SELLER_REQUEST_STATUS["APPROVED"],
                    "seller_request_id": seller_request.id}
        response = c.post("/admin/seller/request/decision", approval)
        response_check = verify_json_response(response.content,
                                              settings.APP_CODE["CALLBACK"])
        self.assertTrue(response_check)
        response_data = simplejson.loads(response.content)
        self.assertEqual(response_data["request_status"],
                         settings.SELLER_REQUEST_STATUS["APPROVED"])

    def test_seller_rejection(self):
        """
        Atleast one pending account needed for this test
        """
        c = logged_in_client()
        seller_request = SellerRequest.objects.filter(
            status=settings.SELLER_REQUEST_STATUS["PENDING"])[0]
        approval = {"decision": settings.SELLER_REQUEST_STATUS["REJECTED"],
                    "seller_request_id": seller_request.id}
        response = c.post("/admin/seller/request/decision", approval)
        response_check = verify_json_response(response.content,
                                              settings.APP_CODE["CALLBACK"])
        self.assertTrue(response_check)
        response_data = simplejson.loads(response.content)
        self.assertEqual(response_data["request_status"],
                         settings.SELLER_REQUEST_STATUS["REJECTED"])
