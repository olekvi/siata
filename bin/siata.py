#!/usr/bin/env python3
''' small script using the API at https://iatacodes.org/
    too find airport and airline names from IATA and ICAO codes
    please see --help for more                                                  '''

import os
import sys
import requests
import argparse

iata_url = 'https://iatacodes.org/api/v6/'

try:
    iata_api_key = os.environ['IATACODES_API_KEY']
except KeyError:
    print('Please set environment variables IATACODES_API_KEY')
    sys.exit(1)

def main():
    p = argparse.ArgumentParser(description='Show data from IATA airport code')
    p.add_argument('-ap', '--airport', type=str, nargs='+',
                        help='one or more IATA code of airport, like OSL')
    p.add_argument('-al', '--airline', type=str, nargs='+',
                        help='one or more IATA code of airline, like SAS')
    a = p.parse_args()

    if a.airport is not None:
        for c in a.airport:
            print(name_from_iata_code('airports',c))

    if a.airline is not None:
        for c in a.airline:
            print(name_from_iata_code('airlines', c))

def name_from_iata_code(query, code):
    r = requests.get(iata_url + query + '?api_key=' +
                                iata_api_key + '&code=' + code)
    d = r.json()
    s = 'IATA ' + code + ': '
    if d['response']:
        s += d['response'][0]['name']
    else:
        s += 'Not found'
    return s

if __name__ == '__main__':
    main()
