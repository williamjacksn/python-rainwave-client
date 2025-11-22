import datetime
import logging
import threading
import typing

from .album import RainwaveAlbum
from .artist import RainwaveArtist
from .dispatch import Signal
from .listener import RainwaveListener
from .request import RainwaveRequest, RainwaveUserRequest, RainwaveUserRequestQueue
from .schedule import RainwaveElection, RainwaveOneTimePlay
from .song import RainwaveSong

if typing.TYPE_CHECKING:
    from . import RainwaveClient, RainwaveSchedule


pre_sync = Signal()
post_sync = Signal()

log = logging.getLogger(__name__)


class RainwaveChannel(dict):
    """A :class:`RainwaveChannel` object represents one channel on the Rainwave
    network.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveClient.channels`.
    """

    def __init__(self, client: "RainwaveClient", raw_info: dict) -> None:
        self._client = client
        try:
            super().__init__(raw_info)
        except ValueError:
            raise Exception(f"Cannot create channel from raw_info {raw_info!r}")
        self._do_sync = False
        self._sync_thread = None

        self._raw_albums = None
        self._albums = None
        self._raw_artists = None
        self._artists = None

        self._sched_current = {}
        self._sched_next = []
        self._sched_history = []
        self._sched_lock = threading.Lock()

        self._raw_requests = []
        self._raw_user_requests = []
        self._requests_lock = threading.Lock()

    def __repr__(self) -> str:
        return f"<RainwaveChannel [{self.name}]>"

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"

    def _do_async_get(self) -> None:
        if not self._stale():
            return
        d = self.client.call("info", {"sid": self.id}, method="GET")
        with self._sched_lock:
            self._sched_current = d["sched_current"]
            self._sched_next = d["sched_next"]
            self._sched_history = d["sched_history"]
        with self._requests_lock:
            self._raw_requests = d["request_line"]
            self._raw_user_requests = d["requests"]
        post_sync.send(self)

    def _do_sync_thread(self) -> None:
        self._do_sync = True
        while self._do_sync:
            pre_sync.send(self)
            args = {"sid": self.id}
            if not self._sched_current:
                args["resync"] = "true"
            d = self.client.call("sync", args)
            missing_data = False
            for key in ["sched_current", "sched_next", "sched_history"]:
                if key not in d:
                    missing_data = True
                    log.error(f"Missing {key} data in API response")
            if missing_data:
                continue
            if self._do_sync:
                with self._sched_lock:
                    self._sched_current = d["sched_current"]
                    self._sched_next = d["sched_next"]
                    self._sched_history = d["sched_history"]
                with self._requests_lock:
                    self._raw_requests = d["request_line"]
                    self._raw_user_requests = d["requests"]
                post_sync.send(self, channel=self)

    def _get_listener_raw_info(self, listener_id: int) -> dict:
        args = {"id": listener_id, "sid": self.id}
        d = self.client.call("listener", args)
        if "listener" in d:
            return d["listener"]
        err = f"There is no listener with id: {listener_id}"
        raise IndexError(err)

    def _new_schedule(self, raw_schedule: dict) -> "RainwaveSchedule":
        if raw_schedule["type"] == "Election":
            return RainwaveElection(self, raw_schedule)
        if raw_schedule["type"] == "OneUp":
            return RainwaveOneTimePlay(self, raw_schedule)

    def _stale(self) -> bool:
        """Return True if timeline information (:attr:`schedule_current`,
        :attr:`schedule_next`, and :attr:`schedule_history`) is missing or out
        of date."""

        if len(self._sched_next) < 1:
            return True
        now = datetime.datetime.now(datetime.timezone.utc)
        ts = self._sched_current["end"]
        ts = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
        return now > ts

    @property
    def albums(self) -> list["RainwaveAlbum"]:
        """A list of :class:`RainwaveAlbum` objects in the playlist of the
        channel."""

        if self._raw_albums is None:
            d = self.client.call("all_albums", {"sid": self.id})
            if "all_albums" in d:
                self._raw_albums = d["all_albums"]
        if self._albums is None:
            self._albums = []
            for raw_album in self._raw_albums:
                new_album = RainwaveAlbum(self, raw_album)
                self._albums.append(new_album)
        return self._albums

    @property
    def artists(self) -> list["RainwaveArtist"]:
        """A list of :class:`RainwaveArtist` objects in the playlist of the
        channel."""

        if self._raw_artists is None:
            d = self.client.call("all_artists", {"sid": self.id})
            if "all_artists" in d:
                self._raw_artists = d["all_artists"]
        if self._artists is None:
            self._artists = []
            for raw_artist in self._raw_artists:
                new_artist = RainwaveArtist(self, raw_artist)
                self._artists.append(new_artist)
        return self._artists

    def clear_rating(self, song_id: int) -> dict:
        args = {"sid": self.id, "song_id": song_id}
        return self.client.call("clear_rating", args)

    @property
    def client(self) -> "RainwaveClient":
        """The :class:`RainwaveClient` object that the channel belongs to."""
        return self._client

    def delete_request(self, song_id: int) -> dict:
        args = {"song_id": song_id, "sid": self.id}
        d = self.client.call("delete_request", args)
        if d["delete_request_result"]["success"]:
            with self._requests_lock:
                self._raw_user_requests = d["requests"]
            return d
        else:
            raise Exception(d["delete_request_result"]["text"])

    @property
    def description(self) -> str:
        """A description of the channel."""
        return self["description"]

    def fave_album(self, album_id: int, fave: bool) -> dict:
        args = {"album_id": album_id, "fave": fave, "sid": self.id}
        return self.client.call("fave_album", args)

    def fave_song(self, song_id: int, fave: bool) -> dict:
        args = {"song_id": song_id, "fave": fave}
        return self.client.call("fave_song", args)

    def get_album_by_id(self, album_id: int) -> "RainwaveAlbum":
        """Return a :class:`RainwaveAlbum` for the given album ID. Raise an
        :exc:`IndexError` if there is no album with the given ID in the
        playlist of the channel.

        :param album_id: the ID of the desired album.
        :type album_id: int
        """

        args = {"sid": self.id, "id": album_id}
        d = self.client.call("album", args)
        if "album_error" in d:
            raise IndexError(d["album_error"]["text"])
        album_data = d["album"]
        if "text" in album_data:
            raise IndexError(album_data["text"])
        return RainwaveAlbum(self, album_data)

    def get_album_by_name(self, name: str) -> "RainwaveAlbum":
        """Return a :class:`RainwaveAlbum` for the given album name. Raise an
        :exc:`IndexError` if there is no album with the given name in the
        playlist of the channel.

        :param name: the name of the desired album.
        :type name: str
        """

        for alb in self.albums:
            if alb.name == name:
                return alb
        error = f"Channel does not contain album with name: {name}"
        raise IndexError(error)

    def get_artist_by_id(self, artist_id: int) -> "RainwaveArtist":
        """Return a :class:`RainwaveArtist` for the given artist ID. Raise an
        :exc:`IndexError` if there is no artist with the given ID in the
        playlist of the channel.

        :param artist_id: the ID of the desired artist.
        :type artist_id: int
        """

        args = {"sid": self.id, "id": artist_id}
        d = self.client.call("artist", args)
        if "id" in d["artist"]:
            return RainwaveArtist(self, d["artist"])
        err = f"Channel does not contain artist with id: {artist_id}"
        raise IndexError(err)

    def get_listener_by_id(self, listener_id: int) -> "RainwaveListener":
        """Return a :class:`RainwaveListener` for the given listener ID. Raise
        an :exc:`IndexError` if there is no listener with the given ID.

        :param listener_id: the ID of the desired listener.
        :type listener_id: int
        """

        raw_listener = self._get_listener_raw_info(listener_id)
        return RainwaveListener(self, raw_listener)

    def get_listener_by_name(self, name: str) -> "RainwaveListener":
        """Return a :class:`RainwaveListener` for the given listener name. Raise
        an :exc:`IndexError` if there is no listener with the given name
        currently listening to the channel.

        :param name: the name of the desired listener.
        :type name: str
        """

        for _listener in self.listeners:
            if _listener.name == name:
                return _listener
        err = f"No current listener named {name}"
        raise IndexError(err)

    def get_song_by_id(self, song_id: int) -> "RainwaveSong":
        """Return a :class:`RainwaveSong` for the given song ID. Raise an
        :exc:`IndexError` if there is no song with the given ID in the playlist
        of the channel.

        :param song_id: the ID of the desired song.
        :type song_id: int
        """

        args = {"sid": self.id, "id": song_id}
        d = self.client.call("song", args)
        if "albums" in d["song"]:
            alb = self.get_album_by_id(d["song"]["albums"][0]["id"])
            return RainwaveSong(alb, d["song"])
        err = f"Channel does not contain song with id: {song_id}"
        raise IndexError(err)

    @property
    def id(self) -> int:
        """The ID of the channel."""
        return self["id"]

    @property
    def key(self) -> str:
        """The channel key, a short string that identifies the channel."""
        return self["key"]

    @property
    def listeners(self) -> list["RainwaveListener"]:
        """A list of :class:`RainwaveListener` objects listening to the channel."""
        d = self.client.call("current_listeners", {"sid": self.id})
        return [RainwaveListener(self, x) for x in d["current_listeners"]]

    @property
    def name(self) -> str:
        """The name of the channel."""
        return self["name"]

    @property
    def ogg_stream(self) -> str:
        """The URL of the OGG stream for the channel. See also
        :attr:`mp3_stream`."""
        return self.mp3_stream.replace(".mp3", ".ogg")

    def rate(self, song_id: int, rating: float) -> dict:
        args = {"sid": self.id, "song_id": song_id, "rating": rating}
        return self.client.call("rate", args)

    def reorder_requests(self, order: list[int]) -> dict:
        args = {"sid": self.id, "order": order}
        d = self.client.call("order_requests", args)
        if d["order_requests_result"]["success"]:
            with self._requests_lock:
                self._raw_user_requests = d["requests"]
            return d
        else:
            raise Exception(d["order_requests_result"]["text"])

    def request_song(self, song_id: int) -> dict:
        args = {"song_id": song_id, "sid": self.id}
        d = self.client.call("request", args)
        if d["request_result"]["success"]:
            with self._requests_lock:
                self._raw_user_requests = d["requests"]
            return d
        else:
            raise Exception(d["request_result"]["text"])

    def clear_requests(self) -> dict:
        return self.client.call("clear_requests", {"sid": self.id})

    @property
    def requests(self) -> list["RainwaveRequest"]:
        """A list of :class:`RainwaveRequest` objects in the request line of
        the channel."""
        if self._stale():
            self._do_async_get()
        rqs = []
        with self._requests_lock:
            for raw_request in self._raw_requests:
                if raw_request.get("song_id") is None:
                    continue
                _song = self.get_song_by_id(raw_request["song_id"])
                _requester = self.get_listener_by_id(raw_request["user_id"])
                rq = RainwaveRequest.request_from_song(_song, _requester)
                rqs.append(rq)
        return rqs

    @property
    def schedule_current(self) -> "RainwaveSchedule":
        """The current :class:`RainwaveSchedule` for the channel."""
        if self._stale():
            self._do_async_get()
        with self._sched_lock:
            sched_current = self._new_schedule(self._sched_current)
        return sched_current

    @property
    def schedule_history(self) -> list["RainwaveSchedule"]:
        """A list of the past :class:`RainwaveSchedule` objects for the channel. The
        events are sorted reverse-chronologically: the first event in the list was the
        most recent event."""
        if self._stale():
            self._do_async_get()
        sched_history = []
        with self._sched_lock:
            sched_history.extend([self._new_schedule(x) for x in self._sched_history])
        return sched_history

    @property
    def schedule_next(self) -> list["RainwaveSchedule"]:
        """A list of the next :class:`RainwaveSchedule` objects for the channel. The
        events are sorted chronologically: the first event in the list will happen
        soonest."""
        if self._stale():
            self._do_async_get()
        sched_next = []
        with self._sched_lock:
            sched_next.extend([self._new_schedule(x) for x in self._sched_next])
        return sched_next

    def start_sync(self) -> None:
        """Begin syncing the timeline for the channel."""

        self.stop_sync()
        self._sync_thread = threading.Thread(target=self._do_sync_thread)
        self._sync_thread.daemon = True
        self._sync_thread.start()

    def stop_sync(self) -> None:
        """Stop syncing the timeline for the channel."""

        self._do_sync = False
        self._sync_thread = None

    @property
    def mp3_stream(self) -> str:
        """The URL of the MP3 stream for the channel. See also
        :attr:`ogg_stream`."""
        return self["stream"]

    @property
    def url(self) -> str:
        """The URL of the web interface for the channel."""
        return f"https://rainwave.cc/{self.key}/"

    @property
    def user_requests(self) -> "RainwaveUserRequestQueue":
        """A :class:`RainwaveUserRequestQueue` of :class:`RainwaveUserRequest`
        objects in the listener's personal request queue."""
        if self._stale():
            self._do_async_get()
        rqs = RainwaveUserRequestQueue(self)
        with self._requests_lock:
            for raw_request in self._raw_user_requests:
                album_id = raw_request["albums"][0]["id"]
                alb = self.get_album_by_id(album_id)
                rq = RainwaveUserRequest(alb, raw_request)
                rqs.append(rq)
        return rqs

    def vote(self, entry_id: int) -> dict:
        args = {"entry_id": entry_id, "sid": self.id}
        return self.client.call("vote", args)
