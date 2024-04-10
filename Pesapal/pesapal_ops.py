from . import pesapal_processor


def post_transaction(Reference, FirstName, LastName, Email, PhoneNumber, Description, Amount, Type):
    oauth_consumer_key = ""
    oauth_consumer_secret = ""
    oauth_callback = ''

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
