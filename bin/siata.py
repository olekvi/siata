#!/usr/bin/env python3
''' small script using the API at https://iatacodes.org/ and http://www.icao.int/
    too find airport and airline names from IATA and ICAO codes
    please see --help for more                                                  '''

import os
import sys
import requests
import argparse

iata_url = 'https://iatacodes.org/api/v6/'
icao_url = 'https://v4p4sz5ijk.execute-api.us-east-1.amazonaws.com/anbdata/'
try:
    iata_api_key = os.environ['IATACODES_API_KEY']
    icao_api_key = os.environ['ICAOCODES_API_KEY']
except KeyError:
    print('Please set environment variables IATACODES_API_KEY and ICAOCODES_API_KEY')
    sys.exit(1)

def main():
    p = argparse.ArgumentParser(
            description='Show data from IATA or ICAO airport code')
    p.add_argument('-ap', '--airport', type=str, nargs='+',
            help='one or more IATA or ICAO code of airport, like OSL ENGM')
    p.add_argument('-al', '--airline', type=str, nargs='+',
            help='one or more IATA or ICAO code of airline, like SAS SK')
    a = p.parse_args()

    if a.airport is not None:
        for c in a.airport:
            print(name_from_iata_code('airports',c))
            print(name_from_icao_code('airports/locations/indicators-list',
                                        'airports', c))

    if a.airline is not None:
        for c in a.airline:
            print(name_from_iata_code('airlines', c))
            print(name_from_icao_code('airlines/designators/code-list',
                                        'operators', c))


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

def name_from_icao_code(query, param, code):
    r = requests.get(icao_url + query + '?api_key=' +
                                icao_api_key + '&' + param + '=' + code)
    d = r.json()
    s = 'ICAO ' + code + ': '
    if d and param == 'airports':
        s += d[0]['airportName'] + ', ' + d[0]['cityName'] + ', ' + d[0]['countryName']
    elif d and param == 'operators':
        s += d[0]['operatorName']
    else:
        s += 'Not found'
    return s

if __name__ == '__main__':
    main()
