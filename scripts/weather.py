from yahoo_weather.weather import YahooWeather
import os
import yaml


class commuteWeather(YahooWeather):
    """ Currently it is a subclass
    of YahooWeather and has no addiontional functionality"""

    conf=None

    def __init__(self):
        self.__load_confs()
        if self.conf:
            super(commuteWeather, self).__init__(
                    APP_ID=self.conf.get(
                        'app_id',None),
                    api_key=self.conf.get(
                        'api_key', None),
                    api_secret=self.conf.get(
                        'api_secret', None)
                    )


    def __load_confs(self):
        """ A method to load Yahoo API credentials"""

        config=os.path.join(os.path.expanduser('~'), '.trafficpatterns.yml')
        with open(config, 'r') as f:
            confs=yaml.safe_load(f)

        self.conf=confs.get('Yahoo', None)
