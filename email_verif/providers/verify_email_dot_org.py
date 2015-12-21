#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging
logger = logging.getLogger(__name__)

from .base import EmailVerifAPIProvider


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

    def set_credentials(self, username=None, password=None, **kwargs):
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
