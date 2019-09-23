from __future__ import unicode_literals

import json
import logging
import sys
import uuid

from . import channel

if sys.version_info[0] == 2:
    from urllib import urlencode
    from urllib2 import urlopen, HTTPError, Request
else:
    from urllib.error import HTTPError
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode

log = logging.getLogger(__name__)


class RainwaveClient:
    """A :class:`RainwaveClient` object provides a simple interface to the
    Rainwave API (see https://rainwave.cc/api4/ for details about the API).

    :param user_id: the User ID to use when communicating with the API.
    :param key: the API key to use when communicating with the API.
    """

    #: The URL upon which all API calls are based.
    base_url = 'https://rainwave.cc/api4/'

    #: The format string used to build canonical album art URLs.
    art_fmt = 'https://rainwave.cc{0}_320.jpg'

    def __init__(self, user_id=None, key=None):
        if user_id is not None:
            self._user_id = int(user_id)
        if key is not None:
            self._key = key
        self._raw_channels = None
        self._channels = None
        self.user_agent = uuid.uuid4().hex

    def __repr__(self):
        msg = 'RainwaveClient(user_id={0!r}, key={1!r})'
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
          >>> rw.call('album', {'id': 1, 'sid': 5})
          {'album': {'name': 'Bravely Default: Flying Fairy', ...}}
        """

        url = '{0}{1}'.format(self.base_url, path.lstrip('/'))

        if args is None:
            args = {}
        if 'user_id' not in args and self.user_id:
            args['user_id'] = self.user_id
        if 'key' not in args and self.key:
            args['key'] = self.key

        data = urlencode(args).encode()
        headers = {'user-agent': self.user_agent}
        req = Request(url=url, data=data, headers=headers)
        try:
            response = urlopen(req)
        except HTTPError as e:
            response = e
        body = response.read().decode(encoding='utf-8')
        api_response = json.loads(body)
        log.debug(api_response)
        return api_response

    @property
    def channels(self):
        """A list of :class:`RainwaveChannel` objects associated with this
        :class:`RainwaveClient` object."""

        if self._raw_channels is None:
            d = self.call('stations')
            if 'stations' in d:
                self._raw_channels = d['stations']
            else:
                raise Exception

        if self._channels is None:
            self._channels = list()
            for raw_channel in self._raw_channels:
                new_channel = channel.RainwaveChannel(self, raw_channel)
                self._channels.append(new_channel)

        return self._channels

    @property
    def key(self):
        """The API key to use when communicating with the API. Find your API
        key at http://rainwave.cc/keys/."""
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def user_id(self):
        """The User ID to use when communicating with the API. Find your User ID
        at http://rainwave.cc/keys/."""
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value
