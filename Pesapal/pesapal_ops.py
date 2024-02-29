from . import pesapal_processor


def post_transaction(Reference, FirstName, LastName, Email, PhoneNumber, Description, Amount, Type):
    oauth_consumer_key = "nRZXsEDVT2uMetIZxnusQPOA4zHyBtlV"
    oauth_consumer_secret = "UzKwzyN9GbXgSNC8HKcMHrJusME="
    oauth_callback = "http://767e1295.ngrok.io/payment/oauth_callback/"

    pesapal = pesapal_processor.PesaPal(oauth_consumer_key, oauth_consumer_secret, 'sandbox')
    pesapal.reference = Reference
    pesapal.last_name = LastName
    pesapal.first_name = FirstName
    pesapal.amount = Amount
    pesapal.type_=Type
    pesapal.phone_number = PhoneNumber
    pesapal.email = Email
    pesapal.callback_url = oauth_callback
    iframe_src = pesapal.generate_iframe_src()
    return iframe_src