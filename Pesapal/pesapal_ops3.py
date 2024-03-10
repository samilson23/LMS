import urllib.request

import requests
from django.conf import settings

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


def get_payment_status1(self, **kwargs):

        """
        Query the payment status from pesapal using the `transaction_id`
        and the `merchant_reference_id`

        Params should include the following keys:
            Required params: `pesapal_merchant_reference`,
            `pesapal_transaction_tracking_id`
        """

        params = {
            "pesapal_merchant_reference": "",
            "pesapal_transaction_tracking_id": "",
        }

        params.update(**kwargs)

        signed_request = self.sign_request(params, settings.PESAPAL_QUERY_STATUS_LINK)

        url = signed_request.to_url()

        response = requests.get(
            url, headers={"content-type": "text/namevalue; charset=utf-8"}
        )
        if response.status_code != requests.codes.ok:
            comm_status = False
        else:
            comm_status = True

        response_data = {}
        response_data["raw_request"] = url
        response_data["raw_response"] = response.text
        response_data["comm_success"] = comm_status

        _, values = response.text.split("=")
        if values == 'INVALID':
            response_data["payment_status"] = values
            return response_data

        _, payment_method, status, _ = values.split(",")
        response_data["payment_status"] = status
        response_data["payment_method"] = payment_method

        return response_data


def process_payment_status(self):
    params = self.get_params()

    self.transaction = get_object_or_404(
        merchant_reference=self.merchant_reference,
        pesapal_transaction=self.transaction_id,
    )

    # check status from pesapal server
    response = self.get_payment_status(**params)