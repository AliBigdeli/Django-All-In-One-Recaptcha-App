import json
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener

from .app_settings import RECAPTCHA_DOMAIN,RECAPTCHA_PROXY,RECAPTCHA_VERIFY_REQUEST_TIMEOUT


class RecaptchaResponse:
    def __init__(self, is_valid, error_codes=None, extra_data=None):
        self.is_valid = is_valid
        self.error_codes = error_codes or []
        self.extra_data = extra_data or {}


def recaptcha_request(params):
    
    
    request_object = Request(
        url=f"https://{RECAPTCHA_DOMAIN}/recaptcha/api/siteverify" ,
        data=params,
        headers={
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Django",
        },
    )
    

    # Add proxy values to opener if needed.
    opener_args = []
    proxies = RECAPTCHA_PROXY
    if proxies:
        opener_args = [ProxyHandler(proxies)]
    opener = build_opener(*opener_args)

    return opener.open(
        request_object,
        timeout=RECAPTCHA_VERIFY_REQUEST_TIMEOUT,
    )



def submit(recaptcha_response, private_key, remoteip):
    """
    Submits a reCAPTCHA request for verification. Returns RecaptchaResponse
    for the request
    recaptcha_response -- The value of reCAPTCHA response from the form
    private_key -- your reCAPTCHA private key
    remoteip -- the user's ip address
    """
    params = urlencode(
        {
            "secret": private_key,
            "response": recaptcha_response,
            "remoteip": remoteip,
        }
    )

    params = params.encode("utf-8")

    response = recaptcha_request(params)
    data = json.loads(response.read().decode("utf-8"))
    response.close()
    return RecaptchaResponse(
        is_valid=data.pop("success"),
        error_codes=data.pop("error-codes", None),
        extra_data=data,
    )