#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import json
import os


def store_addresses(url):

    response = requests.get(url)

    if response:
        soup = BeautifulSoup(response.text)

        rows = soup.find_all('tr')
        import pdb
        pdb.set_trace()
        # collect only unique addresses
        routes = set()
        for row in rows:
            row_data = row.find_all('td')
            try:
                routes.add(row_data[1].text)
                routes.add(row_data[2].text)
                for item in row_data[3].text.split(". "):
                    routes.add(item)
            except:
                # TODO: Donot silently fail
                continue

        # json ops
        routes_for_json = {'addresses': [x for x in routes]}
        # existing json is appended
        if os.path.isfile('addresses.json'):
            with open('addresses.json', 'r') as f:
                routes_deserialized = json.load(f)
            routes_deserialized['addresses'].extend(
                routes_for_json['addresses'])
            routes_for_json = routes_deserialized

        routes_json = json.dumps(routes_for_json, indent=4)

        # put the page results in a file
        # TODO: Need to remove duplicate values from results
        with open('addresses.json', 'w') as f:
            f.write(routes_json)
            routes = None


def collect_routes(base_page_url):
    base_page = requests.get(base_page_url)
    doc = BeautifulSoup(base_page.text)
    routes = [base_page_url + ",{}".format(link.attrs['href'].split(',')[1])
              for link in doc.find_all('a')
              if link.text is not '' and 'Routes ' in link.text]

    return routes


if __name__ == "__main__":

    if os.path.isfile('addresses.json'):
        os.remove('addresses.json')

    urls = collect_routes('https://en.wikipedia.org/wiki/List_of_BMTC_routes')
    for url in urls:
        store_addresses(url)
