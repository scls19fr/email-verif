#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging
logger = logging.getLogger(__name__)

from .base import EmailVerif

from .verify_email_dot_org import EmailVerifProviderVerifyEmailDotOrg
from .email_hippo_dot_com import EmailVerifProviderEmailHippoDotCom
from .email_validator_dot_net import EmailVerifProviderEmailValidatorDotNet


from collections import OrderedDict


_D_VERIFIERS = OrderedDict()


def Verifier(provider):
    try:
        verif_cls = _D_VERIFIERS[provider]
        return verif_cls
    except KeyError:
        raise NotImplementedError("provider '%s' not in %s" % (provider, list(_D_VERIFIERS.keys())))


def register(provider, cls_provider):
    assert issubclass(cls_provider, EmailVerif), \
        "'%s' must be subclass of '%s'" % (cls_provider, EmailVerif)
    _D_VERIFIERS[provider] = cls_provider


def register_all():
    register('verify-email.org', EmailVerifProviderVerifyEmailDotOrg)
    register('emailhippo.com', EmailVerifProviderEmailHippoDotCom)
    register('email-validator.net', EmailVerifProviderEmailValidatorDotNet)


register_all()
