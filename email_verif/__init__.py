#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import requests
import six
from collections import OrderedDict
class EmailVerif(object):
    def __init__(self):
        pass

    def verify(self, emails):
        """
        Verify one or several emails
        """
        if isinstance(emails, six.string_types):
            results = self._verify_email_one(emails)
        else:
            results = self._verify_email_multi(emails)
        return results

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

class EmailVerifVerifyEmail(EmailVerif):
    def __init__(self, session=None):
        super(EmailVerifVerifyEmail, self).__init__()
        self.session = self._init_session(session)

    @property
    def base_url(self):
        return 'http://api.verify-email.org'

    @property
    def endpoint(self):
        return '/api.php'

    @property
    def url(self):
        return self.base_url + self.endpoint

    def _init_session(self, session):
        """
        Returns a requests.Session or session
        """
        if session is None:
            session = requests.Session()
        return session

    def _get_params(self, check):
        """
        Returns dict of parameters to send to API
        
        Parameters:
        ==========
        check: email to check (string)

        """
        return {
            'usr': self._username,
            'pwd': self._password,
            'check': check
        }

    def set_credentials(self, username=None, password=None):
        """
        Set credentials
        """
        self._username = username
        self._password = password

    def _verify_email_one(self, email):
        params = self._get_params(email)
        response = self.session.get(self.url, params=params)
        status_code = response.status_code
        status_code_expected = requests.codes.ok
        if status_code == status_code_expected:
            json_response = response.json()
            parsed_json_response = self._parse_json_response(json_response)
            return parsed_json_response
        else:
            raise("Status code is %d instead of %d" % (status_code, status_code_expected))

    def _parse_json_response(self, response):
        for key in ('authentication_status', 'limit_status', 'verify_status'):
            response[key] = bool(response[key])      
        return response
