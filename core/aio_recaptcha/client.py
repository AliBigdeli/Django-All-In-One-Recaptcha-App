import json
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener
from urllib.error import URLError
from .app_settings import (
    RECAPTCHA_DOMAIN,
    RECAPTCHA_PROXY,
    RECAPTCHA_VERIFY_REQUEST_TIMEOUT,
)


class RecaptchaResponse:
    def __init__(self, is_valid, error_codes=None, extra_data=None):
        self.is_valid = is_valid
        self.error_codes = error_codes or []
        self.extra_data = extra_data or {}


def recaptcha_request(params):
    request_object = Request(
        url=f"https://{RECAPTCHA_DOMAIN}/recaptcha/api/siteverify",
        data=params,
        headers={
            "Content-type": "application/x-www-form-urlencoded",
            "User-agent": "reCAPTCHA Django",
        },
    )

    # holding args for opener
    opener_args = []

    # adding proxies if available
    proxies = RECAPTCHA_PROXY
    if proxies:
        opener_args = [ProxyHandler(proxies)]

    # building opener adn making it ready
    opener = build_opener(*opener_args)

    # creating request object
    return opener.open(
        request_object,
        timeout=RECAPTCHA_VERIFY_REQUEST_TIMEOUT,
    )


def submit(recaptcha_response, secret_key, remoteip):
    """
    Submits a reCAPTCHA request for verification.
    Returns RecaptchaResponse
    (
        recaptcha_response :The value of reCAPTCHA response from the form
        secret_key -- your reCAPTCHA private key
        remoteip -- the user's ip address
    ) --> returning the response object
    """
    # encoding url params
    params = urlencode(
        {
            "secret": secret_key,
            "response": recaptcha_response,
            "remoteip": remoteip,
        }
    )

    # changing encode to utf-8 for compability
    params = params.encode("utf-8")

    # try sending the request if it fails it will handle as a browser error
    try:
        response = recaptcha_request(params)
    except URLError:
        return RecaptchaResponse(
            is_valid=False,
            error_codes=["browser-error"],
            extra_data=None,
        )

    # loading response as a json object
    data = json.loads(response.read().decode("utf-8"))
    """
    'success': # either true for successful or false for unsuccessful
    'challenge_ts': # datetime of request challenge
    'hostname': # host name of the server
    'score': # result of score
    'action': # will be 'form' in django forms or action name you choose in api
    """

    # closing the request
    response.close()

    # returning the result of challenge
    return RecaptchaResponse(
        is_valid=data.pop("success"),
        error_codes=data.pop("error-codes", None),
        extra_data=data,
    )
