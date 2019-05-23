#!/usr/bin/env python

from scripts.finder import GoogleMap
import os
import json
import sys
import unittest

class Coordinates_test(unittest.TestCase):

    def setUp(self):
        self.map = GoogleMap()
        dirname=os.path.join(os.path.dirname(__file__))
        dirname=os.path.dirname(dirname)

        with open(os.path.join(dirname,'data/addresses.json'), 'r') as f:
            address_desr = json.load(f)
        self.addr = address_desr['addresses'][0]

    def test_coord(self):
        result = self.map.geocode(self.addr)
        lat = result[0]['geometry']['location']['lat']
        lng = result[0]['geometry']['location']['lng']

        self.assertTrue([lat, lng])


if __name__ == "__main__":
    unittest.main()
