#!/usr/bin/env python
# encoding: utf-8
"""
Created by 'bens3' on 2013-06-21.
Copyright (c) 2013 'bens3'. All rights reserved.
"""


import re
import sys
import os
import requests
import requests_cache
from bs4 import BeautifulSoup

DATASET_ID = '7e380070-f762-11e1-a439-00145eb45e9a'
OFFSET_INTERVAL = 10


def main():

    requests_cache.install_cache('_cache/gbif')
    offset = 0
    total = 0
    while True:
        print 'Retrieving page offset %s' % offset
        # Build URL
        url = os.path.join('http://www.gbif.org/dataset', DATASET_ID, 'activity')
        r = requests.get(url,  params={'offset': offset})
        # Get some soup
        soup = BeautifulSoup(r.content)
        # Find the bit with the record count
        dts = soup.findAll("dt", text="Records")
        if dts:
            for dt in dts:
                total += int(re.search(r'(\d+)', dt.find_next('dd').text).group(1))
        else:
            # Nothing found, probable the last record
            print 'No records found for offset %s. Exiting.' % offset
            break;
        # Increment offset by interval
        offset += OFFSET_INTERVAL
    print 'TOTAL RECORD DOWNLOADS: %s' % total

if __name__ == '__main__':
    main()

