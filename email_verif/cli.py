#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python bin/email_verif --username YOURUSERNAME --password YOURPASSWORD --emails foo.bar.1@domain.com,foo.bar.2@domain.com,foo.bar.3@domain.com,foo.bar.4@domain.com
"""

from __future__ import absolute_import, division, print_function

import click

import os
from email_verif import Verifier

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
@click.option('--filename', default='', help='Excel file with emails')
@click.option('--column', default='Email', help='Email column')
@click.option('--username', default='', help='Username')
@click.option('--password', default='', help='Password')
@click.option('--api_key', default='', help='API key')
@click.option('--api_url', default='', help='API URL')
@click.option('--bulk', default=False, help='API URL')
def main(provider, emails, filename, column, username, password, api_key, api_url, bulk):
    logging.basicConfig(level=logging.DEBUG)

    pp = pprint.PrettyPrinter(indent=4)
    if emails != '':
        emails = emails.split(',')
    else:
        if filename != '':
            short_file_name, file_extension = os.path.splitext(filename)
            if _HAS_PANDAS:
                if file_extension in ['.xls', '.xlsx']:
                    df = pd.read_excel(filename)
                    emails = df[column].values
                elif file_extension in ['.csv']:
                    df = pd.read_csv(filename)
                    emails = df[column].values
                else:
                    raise NotImplementedError("Filename extension must be '.xls', '.xlsx' or '.csv'")
            else:
                raise NotImplementedError("Pandas is necessary to feed emails using Excel or CSV file")
        else:
            raise NotImplementedError("No emails where given")

    print("Create a CachedSession")
    session = requests_cache.CachedSession(
        cache_name='cache', backend='sqlite', 
        expire_after=datetime.timedelta(days=365))

    print("Instantiate an email verificator")
    verificator = Verifier(provider=provider)(session=session)

    print("Set credentials")
    credentials = {}
    if username != '':
        credentials['username'] = username
    if password != '':
        credentials['password'] = password
    if api_key != '':
        credentials['api_key'] = api_key
    if api_url != '':
        credentials['api_url'] = api_url
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
