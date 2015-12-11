#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from email_verif import EmailVerifVerifyEmail
from config import credentials

import datetime
import requests_cache
# requests_cache is an optional requirements but highly recommanded
# to avoid too much API requests

import pprint

def main():
    pp = pprint.PrettyPrinter(indent=4)

    print("Create a CachedSession")
    session = requests_cache.CachedSession(
        cache_name='cache', backend='sqlite', 
        expire_after=datetime.timedelta(days=365))

    print("Instantiate an email verificator")
    verificator = EmailVerifVerifyEmail(session=session)

    print("Set credentials")
    verificator.set_credentials(
        username=credentials['username'], 
        password=credentials['password']
    )

    #print("Verify one email")
    #results = verificator.verify('foo.bar@domain.com')
    #print(results)

    print("Verify several emails")
    results = verificator.verify(['foo.bar.1@python.org',
                'foo.bar.2@python.org',  'foo.bar.3@python.org', 'email@example.com'])
    pp.pprint(results)

    import pandas as pd
    df_results = pd.DataFrame(results).transpose()
    print(df_results)
    df_results.to_excel("email_valid_results.xls")

if __name__ == "__main__":
    main()
