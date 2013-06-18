import requests

import channel


class RainwaveClient(object):
    '''A RainwaveClient object provides a simple interface to the Rainwave API
    (see http://rainwave.cc/api/ for details about the API)'''

    def __init__(self):
        self.base_url = u'http://rainwave.cc/'
        self.user_id = 0
        self.key = u''
        self.req = requests.Session()

    def call(self, path, args=dict()):
        '''Make a direct call to the API if you know the necessary path and
        arguments'''

        final_url = self.base_url + path.lstrip(u'/')
        if u'user_id' not in args and self.user_id:
            args[u'user_id'] = self.user_id
        if u'key' not in args and self.key:
            args[u'key'] = self.key

        if path.endswith((u'/get', u'/stations')):
            d = self.req.get(final_url)
        else:
            d = self.req.post(final_url, params=args)

        if d.ok:
            return d.json()
        else:
            d.raise_for_status()

    @property
    def channels(self):
        if not hasattr(self, u'_raw_channels'):
            if self.user_id and self.key:
                args = {u'user_id': self.user_id, u'key': self.key}
                self._raw_channels = self.call(u'async/1/stations_user', args)
            else:
                self._raw_channels = self.call(u'async/1/stations')

        if not hasattr(self, u'_channels'):
            self._channels = []
            for raw_channel in self._raw_channels[u'stations']:
                new_channel = channel.RainwaveChannel(self, raw_channel)
                self._channels.append(new_channel)

        return self._channels
