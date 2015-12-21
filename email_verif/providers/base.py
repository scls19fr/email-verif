#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging
logger = logging.getLogger(__name__)

import six
import requests
from abc import ABCMeta, abstractmethod
from collections import OrderedDict


class EmailVerif(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

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
            msg = "Status code is '%d' instead of '%d'" % (status_code, status_code_expected)
            raise(Exception(msg))

    def _parse_json_response(self, response):
        return response
