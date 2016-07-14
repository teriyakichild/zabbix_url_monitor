#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from requests_oauthlib import OAuth1
import packaging
from jpath import jpath


class AuthException(Exception):
    pass

import packaging
from jpath import jpath


class AuthException(Exception):
    pass

def get_hostport_tuple(dport, dhost):
    """
    Tool to take a hostport combination 'localhost:22' string
    and return a tuple ('localhost', 22). If no : seperator
    is given then assume a default port passed as argv1

    :param dport:   A default port to insert into the tuple if not parsable.
    :param dhost:   A host to split ':' on and try to break into a tuple.
    :return:        (hostname,port) <tuple>
    """
    # Detect if port is designated
    if ":" in dhost:
        host = dhost.split(':')[0]
        port = int(dhost.split(':')[1])
        return host, port
    else:  # Use default port
        return dhost, dport


def string2bool(allegedstring):
    """
    Tries to return a boolean from a string input if possible,
    else it just returns the original item, allegedly a string.

    :param allegedstring:   String you are checking
    :return:                the mostly a boolean object
    """
    if allegedstring.lower().startswith('t'):
        return True
    elif allegedstring.lower().startswith('f'):
        return False
    elif allegedstring == "1":
        return True
    elif allegedstring == "0":
        return False
    else:
        return allegedstring


def omnipath(data_object, type, element, throw_error_or_mark_none='none'):
    """
    Used to pull path expressions out of json or java path.
    :param data_object:
    :param type:
    :param element:
    :param throw_error_or_mark_none:
    :return:
    """
    value = None
    if type == 'json':
        try:
            value = jpath(data_object, element['jsonvalue'])

        except:
            if throw_error_or_mark_none == 'none':
                value = None
            else:
                raise KeyError
    if type == 'xml':
        raise NotImplementedError('Be the first to implement xpath.')

    metric = value
    return metric


class WebCaller(object):
    """
    Performs web functions for API's we're running check"s on
    """

    def __init__(self, logging):
        """
        Initialize web instance.
        Bring logging instance in.
        Set session.auth and session_headers to none by default

        :param logging:              Takes the logger object.
        """
        self.logging = logging  # Make instanciation argv local scope

        self.session = None
        self.session_headers = None

    def auth(self, config, identity_provider):
        """
        Start a requests session with this instance.
        This is where we apply authentication schemes.
        If you pass in 'none' or another builtin that is applied.

        :param config:              Focus config into scope
        :param identity_provider:   This is the identity provider key
        :return:                    none <nonetype>
        """
        identity_providers = config['identity_providers']
        try:
            identity_provider = identity_providers[identity_provider]
            auth_kwargs = identity_provider.values()[0]
        except KeyError as err:
            error = str(err) + " defined in testSet as identity_provider but is undeclared in identity_providers!"
            self.logging.exception("KeyError: " + str(err) + str(error))
            raise AuthException(error)

        # If provider is undefined, we get TypeError
        try:
            provider_name = str([x for x in identity_provider][0]).lower()
        except TypeError:
            provider_name = "none"

        self.session = requests.Session()
        self.session_headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            'user-agent': 'python/url_monitor v' + packaging.version + ' (A zabbix monitoring plugin)'
        }
        if provider_name == "none":
            self.session.auth = None

        elif provider_name == "httpbasicauth":
            self.session.auth = HTTPBasicAuth(**auth_kwargs)

        elif provider_name == "httpdigestauth":
            self.session.auth = HTTPDigestAuth(**auth_kwargs)

        elif provider_name == "oauth1":
            self.session.auth = OAuth1(**auth_kwargs)

        else:
            # We must assume we want to load in the format of
            # requests_python_module/requestAuthClassname from the config entry.
            # Split the / to determine import statements t.
            try:
                module_strname = [x for x in identity_provider][0].split('/')[0]
                class_strname = [x for x in identity_provider][0].split('/')[1]
            except IndexError as err:
                error = ("{provider}` is incomplete missing '/' char to "
                         "seperate Module_Name from Class_Name").format(
                    provider=provider_name
                )
                self.logging.exception("IndexError: " + str(err) + str(error))

            # Try to import the specified module
            try:
                _module = __import__(module_strname)
            except ImportError as err:
                error = (
                    "{module_strname}/{class_strname} might be an invalid "
                    "module/class pairing at {module_strname}"
                ).format(
                    module_strname=module_strname,
                    class_strname=class_strname
                )
                self.logging.exception("ImportError: " + str(err) + str(error))

            # And try to reference a class instance
            try:
                external_requests_auth_class = getattr(_module, class_strname)
            except AttributeError as err:
                error = (
                    "{module_strname}.{class_strname} might be an invalid "
                    "class name at {class_strname}"
                ).format(
                    module_strname=module_strname,
                    class_strname=class_strname
                )
                self.logging.exception(
                    "AttributeError: " + str(err) + str(error))

            # Set the external auth handler.
            self.session.auth = external_requests_auth_class(**auth_kwargs)

    def run(self, config, url, verify, expected_http_status, identity_provider, timeout):
        """
        Executes a http request to gather the data.
        expected_http_status can be a list of expected codes.
        :param config:               Focus config into scope
        :param url:                  URI/URL resource
        :param verify:               SSL verify true/false or path to certfile
        :param expected_http_status: A string that is comma seperated of http codes
        :param identity_provider:    This is passed in for 
        :param timeout:              Timeout in seconds to send to requests lib
        :return:                     request <object>
        """

        self.auth(config, identity_provider)
        request = self.session.get(
            url, headers=self.session_headers, verify=verify, timeout=timeout
        )

        # Turns comma seperated string from config to a list, then lower it
        expected_codes = [c.lower() for c in expected_http_status.split(',')]

        # Cast response code into a list
        resp_code = str(request.status_code).split()

        if 'any'.lower() in expected_codes:
            # Allow any HTTP code ranges within RFC 2616 - Hypertext Transfer
            # Protocol -- HTTP/1.1
            expected_codes.remove('any')
            codes = [
                range(100, 104),  # Informational
                range(200, 227),  # Success!
                range(300, 309),  # Redirection
                range(400, 452),  # Client Error
                range(500, 511),  # Internal Error
            ]
            for code in codes:
                expected_codes += code
            expected_codes = map(str, expected_codes)

        # filter returns empty if code not found, returns found expected_codes
        # if they are found.
        valid_response_code = filter(lambda item: any(
            x in item for x in resp_code), expected_codes)

        if not valid_response_code:
            error =  """Bad HTTP response. Expected one of {expect} recieved {got}""".format(
                expect=expected_codes, got=resp_code)
            self.logging.exception(error)
        return request
