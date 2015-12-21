#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging
logger = logging.getLogger(__name__)

from .base import EmailVerifAPIProvider


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
