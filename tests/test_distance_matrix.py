#!/usr/bin/env python

import unittest
from scripts.finder import GoogleMap
import datetime
import os
import json


class TestDistanceMatrix(unittest.TestCase):

    def setUp(self):
        self.map = GoogleMap()
        # arrival time since midnight
        t=datetime.time(hour=9, minute=45, second=0)
        self.arrival_time=int(datetime.timedelta(hours=t.hour,
                minutes=t.minute, seconds=t.second).total_seconds())

        # get first 02 addresses from the addressess.json and keep them as
        # origins and destinations
        proj_dir=os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(proj_dir,'data/addresses.json'), 'r') as f:
            addr=json.load(f)

        self.origins = [origin + ' bus stop, bangalore, India' 
                for origin in addr['addresses'][0:2]]
        self.destinations = [destination + ' bus stop, bangalore, India' 
                for destination in addr['addresses'][0:2]]

        self.units='metric'
        self.mode='driving'


    def test_matrix(self):
        matrix_result=GoogleMap().distance_matrix(origins=self.origins,
                destinations=self.destinations,
                mode=self.mode,
                units=self.units)

        self.assertIsNotNone(matrix_result['rows'])

if __name__=="__main__":
    unittest.main()
