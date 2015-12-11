#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from email_verif import EmailVerif
from config import credentials

import datetime
import requests_cache
# requests_cache is an optional requirements but highly recommanded
# to avoid too much API requests

import pprint
import logging

try:
    import pandas as pd
    _HAS_PANDAS = True
except ImportError:
    _HAS_PANDAS = False

def main():
    logging.basicConfig(level=logging.DEBUG)

    pp = pprint.PrettyPrinter(indent=4)

    print("Create a CachedSession")
    session = requests_cache.CachedSession(
        cache_name='cache', backend='sqlite', 
        expire_after=datetime.timedelta(days=365))

    print("Instantiate an email verificator")
    #provider, bulk = 'verify-email.org', False
    #provider, bulk = 'emailhippo.com', False
    provider, bulk = 'email-validator.net', False
    verificator = EmailVerif.select(provider=provider)(session=session)

    print("Set credentials")
    #verificator.set_credentials(
    #    username=credentials[provider]['username'], 
    #    password=credentials[provider]['password']
    #)
    verificator.set_credentials(**credentials[provider])

    #print("Verify one email")
    #email = 'foo.bar@domain.com'
    #results = verificator.verify(email)
    #print(results)

    print("Verify several emails")
    lst_emails = ['foo.bar.1@python.org', 'example@domain.com',
                'foo.bar.2@python.org', 'foo.bar.3@python.org', 'email@example.com']
    results = verificator.verify(lst_emails, bulk=bulk)
    pp.pprint(results)

    if _HAS_PANDAS:
        results_to_dataframe(results)

def results_to_dataframe(results):
    df_results = pd.DataFrame(results).transpose()
    print(df_results)
    df_results.to_excel("email_valid_results.xls")

if __name__ == "__main__":
    main()
