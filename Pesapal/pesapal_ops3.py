import urllib.request

import requests
from django.conf import settings
from django.shortcuts import get_object_or_404

from . import pesapal_processor3

pesapal_processor3.consumer_key = 'HRwr4SWhFF+LrthH83eBpC4t3tMKT37G'
pesapal_processor3.consumer_secret = '8537Msq3uMjkqV8qzKM5eBakmv0='
pesapal_processor3.testing = False


def post_transaction(Reference, FirstName, LastName, Email, PhoneNumber, Description, Amount, Type):
    post_params = {
        'oauth_callback': 'https://samilsonuniversity1-5c5d6f1676ed.herokuapp.com/Student/CompleteTransaction'
    }

    request_data = {
        'Amount': str(Amount),
        'Description': Description,
        'Type': 'MERCHANT',
        'Reference': Reference,
        'PhoneNumber': str(PhoneNumber),
        'Email': Email,
        'FirstName': FirstName,
        'LastName': LastName
    }

    url = pesapal_processor3.postDirectOrder(post_params, request_data)

    return url


def get_detailed_order_status(merchant_reference, transaction_tracking_id):
    post_params = {
        'pesapal_merchant_reference': merchant_reference,
        'pesapal_transaction_tracking_id': transaction_tracking_id
    }
    url = pesapal_processor3.queryPaymentDetails(post_params)
    response = urllib.request.urlopen(url)

    return response.read()


def get_payment_status(merchant_reference, transaction_tracking_id):
    post_params = {
        'pesapal_merchant_reference': merchant_reference,
        'pesapal_transaction_tracking_id': transaction_tracking_id
    }
    url = pesapal_processor3.queryPaymentStatus(post_params)
    response = urllib.request.urlopen(url)

    return response.read()


def get_payment_status_by_mercharnt_ref(merchant_reference):
    post_params = {
        'pesapal_merchant_reference': merchant_reference
    }
    url = pesapal_processor3.queryPaymentStatusByMerchantRef(post_params)
    response = urllib.request.urlopen(url)

    return response.read()
