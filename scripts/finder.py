import os
import requests
import yaml
from googlemaps import Client

class GoogleMap(Client):

    confs=None

    def __init__(self):
        self.confs=self.__get_confs()
        self.api_key=self.confs.get('Gmap', None).get('api_key', None)
        super(GoogleMap, self).__init__(key=self.api_key)

    def __get_confs(self):
        config=os.path.join(os.path.expanduser('~'), '.trafficpatterns.yml')
        with open(config, 'r') as f:
            conf=yaml.safe_load(f)

        return conf
