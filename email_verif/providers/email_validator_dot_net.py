#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging
logger = logging.getLogger(__name__)

from .base import EmailVerifAPIProvider


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
