import requests

from . import channel


class RainwaveClient:
    """A :class:`RainwaveClient` object provides a simple interface to the
    Rainwave API (see http://rainwave.cc/api4/ for details about the API).

    :param user_id: the User ID to use when communicating with the API.
    :param key: the API key to use when communicating with the API.
    """

    #: The URL upon which all API calls are based.
    base_url = 'http://rainwave.cc/api4/'

    #: The User ID to use when communicating with the API. Find your User ID at
    #: http://rainwave.cc/auth/.
    user_id = 0

    #: The API key to use when communicating with the API. Find your API key at
    #: http://rainwave.cc/auth/.
    key = ''

    def __init__(self, user_id=0, key=''):
        self.user_id = user_id
        self.key = key
        self._raw_channels = None
        self._channels = None
        self.req = requests.Session()

    def __repr__(self):
        msg = 'RainwaveClient(user_id={!r}, key={!r})'
        return msg.format(self.user_id, self.key)

    def call(self, path, args=None):
        """Make a direct call to the API if you know the necessary path and
        arguments.

        :param path: the URL path of the API method to call.
        :type path: str
        :param args: (optional) any arguments required by the API method.
        :type args: dict

        Usage::

          >>> from rainwaveclient import RainwaveClient
          >>> rw = RainwaveClient(5049, 'abcde12345')
          >>> rw.call('async/1/album', {'album_id': 1})
          {'playlist_album': {'album_name': 'Wild Arms', ...}}
        """

        if args is None:
            args = dict()
        final_url = self.base_url + path.lstrip('/')
        if 'user_id' not in args and self.user_id:
            args['user_id'] = self.user_id
        if 'key' not in args and self.key:
            args['key'] = self.key

        if path.endswith(('/get', '/stations')):
            d = self.req.get(final_url)
        else:
            d = self.req.post(final_url, params=args)

        if d.ok:
            return d.json()
        else:
            d.raise_for_status()

    @property
    def channels(self):
        """A list of :class:`RainwaveChannel` objects associated with this
        :class:`RainwaveClient` object."""

        if self._raw_channels is None:
            if self.user_id and self.key:
                args = {'user_id': self.user_id, 'key': self.key}
                self._raw_channels = self.call('async/1/stations_user', args)
            else:
                self._raw_channels = self.call('async/1/stations')

        if self._channels is None:
            self._channels = list()
            for raw_channel in self._raw_channels['stations']:
                new_channel = channel.RainwaveChannel(self, raw_channel)
                self._channels.append(new_channel)

        return self._channels
