#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python bin/email_verif --username YOURUSERNAME --password YOURPASSWORD --emails foo.bar.1@domain.com,foo.bar.2@domain.com,foo.bar.3@domain.com,foo.bar.4@domain.com
"""

from __future__ import absolute_import, division, print_function

import click

from email_verif import EmailVerif

import datetime
import requests_cache

import pprint
import logging

try:
    import pandas as pd
    _HAS_PANDAS = True
except ImportError:
    _HAS_PANDAS = False

@click.command()
@click.option('--provider', default='verify-email.org', help='Email verificator provider')
@click.option('--emails', default='', help='Emails')
@click.option('--username', default='', help='Username')
@click.option('--password', default='', help='Password')
@click.option('--api_key', default='', help='API key')
@click.option('--api_url', default='', help='API URL')
def main(provider, emails, username, password, api_key, api_url):
    logging.basicConfig(level=logging.DEBUG)

    pp = pprint.PrettyPrinter(indent=4)
    emails = emails.split(',')

    print("Create a CachedSession")
    session = requests_cache.CachedSession(
        cache_name='cache', backend='sqlite', 
        expire_after=datetime.timedelta(days=365))

    print("Instantiate an email verificator")
    provider, bulk = 'verify-email.org', False
    verificator = EmailVerif.select(provider=provider)(session=session)

    print("Set credentials")
    credentials = {
        'username': username,
        'password': password,
        'api_key': api_key,
        'api_url': api_url
    }
    verificator.set_credentials(**credentials)
    results = verificator.verify(emails, bulk=bulk)
    pp.pprint(results)

    if _HAS_PANDAS:
        results_to_dataframe(results)

def results_to_dataframe(results, filename='email_valid_results.xls'):
    df_results = pd.DataFrame(results).transpose()
    print(df_results)
    df_results.to_excel(filename)

if __name__ == "__main__":
    main()
