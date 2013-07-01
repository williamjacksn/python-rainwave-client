import channel
import requests


class RainwaveClient(object):
    '''A :class:`RainwaveClient` object provides a simple interface to the
    Rainwave API (see http://rainwave.cc/api/ for details about the API).

    :param user_id: the User ID to use when communicating with the API.
    :param key: the API key to use when communicating with the API.
    '''

    #: The URL upon which all API calls are based.
    base_url = u'http://rainwave.cc/'

    #: The User ID to use when communicating with the API. Find your User ID at
    #: http://rainwave.cc/auth/.
    user_id = 0

    #: The API key to use when communicating with the API. Find your API key at
    #: http://rainwave.cc/auth/.
    key = u''

    def __init__(self, user_id=0, key=u''):

        self.user_id = user_id
        self.key = key
        self.req = requests.Session()

    def __repr__(self):
        msg = u'RainwaveClient(user_id={}, key={})'
        return msg.format(self.user_id, repr(self.key))

    def call(self, path, args=dict()):
        '''Makes a direct call to the API if you know the necessary path and
        arguments.

        :param path: the URL path of the API method to call.
        :type path: str
        :param args: (optional) any arguments required by the API method.
        :type args: dict

        Usage::

          >>> from gutter import RainwaveClient
          >>> rw = RainwaveClient(5049, u'abcde12345')
          >>> rw.call(u'async/1/album', {u'album_id': 1})
          {u'playlist_album': {u'album_name': u'Wild Arms', ...}}
        '''

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
        '''A list of :class:`RainwaveChannel` objects associated with this
        :class:`RainwaveClient` object.'''

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
