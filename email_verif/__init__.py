#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import six
from collections import OrderedDict

import requests

from abc import ABCMeta, abstractmethod
import logging

logger = logging.getLogger(__name__)

class EmailVerif(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @classmethod
    def select(cls, provider='verify-email.org'):
        provider = provider.lower()
        d = OrderedDict([
            ('verify-email.org', EmailVerifProviderVerifyEmailDotOrg),
            ('emailhippo.com', EmailVerifProviderEmailHippoDotCom),
            ('email-validator.net', EmailVerifProviderEmailValidatorDotNet),
        ])
        try:
            verif_cls = d[provider]
            return verif_cls
        except KeyError:
            raise NotImplementedError("%s not in %s" % (cls, d.keys()))

    def verify(self, emails, return_failed=False, bulk=False):
        """
        Verify one or several emails
        """
        if isinstance(emails, six.string_types):
            results = self._verify_email_one(emails)
        else:
            if not bulk:
                results = self._verify_email_multi(emails, return_failed=return_failed)
            else:
                results = self._verify_email_multi_bulk(emails)
        return results

    @abstractmethod
    def _verify_email_one(self, email):
        pass

    def _verify_email_multi(self, emails, return_failed=False):
        d_passed = OrderedDict()
        d_failed = OrderedDict()
        for email in emails:
            try:
                d_passed[email] = self._verify_email_one(email)
            except Exception as e:
                d_failed[email] = self._verify_email_one(email)
        if return_failed:
            return d_passed, d_failed
        else:
            return d_passed

class EmailVerifAPIProvider(EmailVerif):
    __metaclass__ = ABCMeta

    def _init_session(self, session):
        """
        Returns a requests.Session or session
        """
        if session is None:
            session = requests.Session()
        return session

    def set_credentials(self, **kwargs):
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def _verify_email_one(self, email):
        params = self._get_params(email)
        logger.debug("GET request to %s with %s" % (self.url, params))
        response = self.session.get(self.url, params=params)
        status_code = response.status_code
        status_code_expected = requests.codes.ok
        if status_code == status_code_expected:
            response = response.json()
            logger.debug("  response: %s" % response)
            response = self._parse_json_response(response)
            return response
        else:
            raise("Status code is %d instead of %d" % (status_code, status_code_expected))

    def _parse_json_response(self, response):
        return response

class EmailVerifProviderVerifyEmailDotOrg(EmailVerifAPIProvider):
    def __init__(self, session=None):
        super(EmailVerifProviderVerifyEmailDotOrg, self).__init__()
        self.session = self._init_session(session)
        self.username = None
        self.password = None

    @property
    def base_url(self):
        return 'http://api.verify-email.org'

    @property
    def endpoint(self):
        return '/api.php'

    @property
    def url(self):
        return self.base_url + self.endpoint

    def _get_params(self, check):
        """
        Returns dict of parameters to send to API
        
        Parameters:
        ==========
        check: email to check (string)

        """
        return {
            'usr': self.username,
            'pwd': self.password,
            'check': check
        }

    def set_credentials(self, username=None, password=None):
        """
        Set credentials

        Parameters:
        ==========
        username: username (string)
        password: password (string)

        """
        self.username = username
        self.password = password

    def _parse_json_response(self, response):
        for key in ('authentication_status', 'limit_status', 'verify_status'):
            try:
                response[key] = bool(response[key])
                if response['authentication_status']:
                    raise NotImplementedError("Authentification failed")
            except Exception as e:
                pass
        return response

class EmailVerifProviderEmailHippoDotCom(EmailVerifAPIProvider):
    def __init__(self, session=None):
        super(EmailVerifProviderEmailHippoDotCom, self).__init__()
        self.session = self._init_session(session)
        self.api_key = None
        self.api_url = None

    def set_credentials(self, api_key=None, api_url=None):
        """
        Set credentials

        Parameters:
        ==========
        api_key: API key (string)
        api_url: API URL (string)

        """
        self.api_key = api_key
        self.api_url = api_url

    @property
    def url(self):
        return self.api_url

    def _get_params(self, emails):
        """
        Returns dict of parameters to send to API
        
        Parameters:
        ==========
        emails: email to check (string)

        """
        return {
            'k': self.api_key,
            'e': emails,
        }

class EmailVerifProviderEmailValidatorDotNet(EmailVerifAPIProvider):
    def __init__(self, session=None):
        super(EmailVerifProviderEmailValidatorDotNet, self).__init__()
        self.session = self._init_session(session)
        self.api_key = None

    @property
    def url(self):
        return 'http://api.email-validator.net/api/verify'

    def _get_params(self, emails, timeout=10):
        """
        Returns dict of parameters to send to API
        
        Parameters:
        ==========
        emails: email to check (string)

        """
        return {
            'APIKey': self.api_key,
            'EmailAddress': emails,
            'Timeout': timeout,
        }

    def _get_data_bulk(self, emails, 
            task_name='', validation_mode='', notify_email='', notify_url=''):
        return {
            'EmailAddress': '\n'.join(emails),
            'APIKey': self.api_key,
            'TaskName': task_name,
            'ValidationMode': validation_mode,
            'NotifyEmail': notify_email,
            'NotifyURL': notify_url
        }

    def _parse_json_response(self, response):
        if response['status'] == 200:
            response['valid'] = True
        else:
            response['valid'] = False
        return response

    def _verify_email_multi_bulk(self, emails):
        url = 'http://bulk.email-validator.net/api/verify'
        data = self._get_data_bulk(emails)
        logger.debug("POST request to %s with data=%s" % (url, data))
        response = self.session.post(self.url, data=data)
        status_code = response.status_code
        status_code_expected = requests.codes.ok
        if status_code == status_code_expected:
            response = response.json()
            logger.debug("  response: %s" % response)
            response = self._parse_json_response(response)
            return response
        else:
            raise("Status code is %d instead of %d" % (status_code, status_code_expected))
