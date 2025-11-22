import json
import logging
import uuid
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .channel import RainwaveChannel

log = logging.getLogger(__name__)


class RainwaveClient:
    """A :class:`RainwaveClient` object provides a simple interface to the
    Rainwave API (see https://rainwave.cc/api4/ for details about the API).

    :param user_id: the User ID to use when communicating with the API.
    :type user_id: int
    :param key: the API key to use when communicating with the API.
    :type key: str
    """

    #: The URL upon which all API calls are based.
    base_url = "https://rainwave.cc/api4/"

    #: The format string used to build canonical album art URLs.
    art_fmt = "https://rainwave.cc{0}_320.jpg"

    def __init__(self, user_id: int | None = None, key: str | None = None) -> None:
        if user_id is not None:
            self._user_id = int(user_id)
        if key is not None:
            self._key = key
        self._raw_channels = None
        self._channels = None
        self.user_agent = uuid.uuid4().hex

    def __repr__(self) -> str:
        return f"RainwaveClient(user_id={self.user_id!r}, key={self.key!r})"

    def call(self, path: str, args: dict | None = None, method: str = "POST") -> dict:
        # noinspection PyUnresolvedReferences
        """Make a direct call to the API if you know the necessary path and
        arguments.

        :param path: the URL path of the API method to call.
        :type path: str
        :param args: (optional) any arguments required by the API method.
        :type args: dict
        :param method: (optional) the HTTP method to use for the API call,
            default `POST`
        :type method: str
        :return: The raw data returned from the API call.
        :rtype: dict

        Usage::

          >>> from rainwaveclient import RainwaveClient
          >>> rw = RainwaveClient(5049, 'abcde12345')
          >>> rw.call('album', {'id': 1, 'sid': 5})
          {'album': {'name': 'Bravely Default: Flying Fairy', ...}}
        """

        path = path.lstrip("/")
        url = f"{self.base_url}{path}"

        if args is None:
            args = {}
        if "user_id" not in args and self.user_id:
            args["user_id"] = self.user_id
        if "key" not in args and self.key:
            args["key"] = self.key

        data = urlencode(args).encode()
        headers = {"user-agent": self.user_agent}
        req = Request(url=url, data=data, headers=headers, method=method)  # noqa: S310
        try:
            log.debug(f"Calling {url}")
            response = urlopen(req)  # noqa: S310
        except HTTPError as e:
            response = e
        body = response.read().decode(encoding="utf-8")
        api_response = json.loads(body)
        log.debug(api_response)
        return api_response

    @property
    def channels(self) -> list[RainwaveChannel]:
        """A list of :class:`RainwaveChannel` objects associated with this
        :class:`RainwaveClient` object."""

        if self._raw_channels is None:
            d = self.call("stations")
            if "stations" in d:
                self._raw_channels = d["stations"]
            else:
                raise Exception

        if self._channels is None:
            self._channels = list()
            for raw_channel in self._raw_channels:
                new_channel = RainwaveChannel(self, raw_channel)
                self._channels.append(new_channel)

        return self._channels

    @property
    def key(self) -> str:
        """The API key to use when communicating with the API. Find your API
        key at https://rainwave.cc/keys/."""
        return self._key

    @key.setter
    def key(self, value: str) -> None:
        self._key = value

    @property
    def user_id(self) -> int:
        """The User ID to use when communicating with the API. Find your User ID
        at https://rainwave.cc/keys/."""
        return self._user_id

    @user_id.setter
    def user_id(self, value: int) -> None:
        self._user_id = value
