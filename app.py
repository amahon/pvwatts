#!/usr/bin/env python

# Use Virutalenv to create virtualenv for project.
# https://virtualenv.pypa.io/en/stable/
# https://virtualenvwrapper.readthedocs.io/en/latest/
# pip install -r requirement.txt

import csv
import requests
import json
import pprint
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("API_KEY")
args = parser.parse_args()

API_KEY = args.API_KEY
BASE_URL = 'https://developer.nrel.gov/api/pvwatts/v5.json?'
INPUT_FILE = 'input.csv'
OUTPUT_FILE = 'output.csv'

output_headers = [
    'city',
    'elev',
    'lat',
    'lon',
    'ac_annual',
    'capacity_factor',
    'solrad_annual'
]
output_rows = [output_headers]

with open(INPUT_FILE, 'r') as f_input:
    input_reader = csv.DictReader(f_input)
    for params in input_reader:
        params['api_key'] = API_KEY
        request = requests.get(BASE_URL, params=dict(params))
        response_data = request.json()
        output_rows.append([
            response_data['station_info']['city'],
            response_data['station_info']['elev'],
            response_data['station_info']['lat'],
            response_data['station_info']['lon'],
            response_data['outputs']['ac_annual'],
            response_data['outputs']['capacity_factor'],
            response_data['outputs']['solrad_annual']
        ])


with open(OUTPUT_FILE, 'w+') as f_output:
    output_writer = csv.writer(f_output)
    output_writer.writerows(output_rows)
