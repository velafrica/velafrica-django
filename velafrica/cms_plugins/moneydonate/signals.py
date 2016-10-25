from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from velafrica.core.settings import PAYPAL_RECEIVER_MAIL


def valid_ipn(sender, **kwargs):
    print('---------- paypal ipn signal call ----------')
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the business field request. (The user could tamper
        # with those fields on payment form before send it to PayPal)
        if ipn_obj.receiver_email != PAYPAL_RECEIVER_MAIL:
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received etc. are all what you expect.

        # Undertake some action depending upon `ipn_obj`.
        if ipn_obj.custom == "Upgrade all users!":
            pass
    else:
        pass

valid_ipn_received.connect(valid_ipn)
