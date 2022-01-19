from __future__ import unicode_literals

import datetime
import threading

from . import album
from . import artist
from . import dispatch
from . import listener
from . import request
from . import schedule
from . import song

pre_sync = dispatch.Signal()
post_sync = dispatch.Signal()


class RainwaveChannel(dict):
    """A :class:`RainwaveChannel` object represents one channel on the Rainwave
    network.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveClient.channels`.
    """

    def __init__(self, client, raw_info):
        self._client = client
        super(RainwaveChannel, self).__init__(raw_info)
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

    def __repr__(self):
        return '<RainwaveChannel [{0}]>'.format(self.name)

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.description)

    def _do_async_get(self):
        if not self._stale():
            return
        d = self.client.call('/info', {'sid': self.id})
        with self._sched_lock:
            self._sched_current = d['sched_current']
            self._sched_next = d['sched_next']
            self._sched_history = d['sched_history']
        with self._requests_lock:
            self._raw_requests = d['request_line']
            self._raw_user_requests = d['requests']
        post_sync.send(self)

    def _do_sync_thread(self):
        self._do_sync = True
        while self._do_sync:
            pre_sync.send(self)
            args = {'sid': self.id}
            if not self._sched_current:
                args['resync'] = 'true'
            d = self.client.call('sync', args)
            if self._do_sync:
                with self._sched_lock:
                    self._sched_current = d['sched_current']
                    self._sched_next = d['sched_next']
                    self._sched_history = d['sched_history']
                with self._requests_lock:
                    self._raw_requests = d['request_line']
                    self._raw_user_requests = d['requests']
                post_sync.send(self, channel=self)

    def _get_listener_raw_info(self, listener_id):
        args = {'id': listener_id, 'sid': self.id}
        d = self.client.call('listener', args)
        if 'listener' in d:
            return d['listener']
        err = 'There is no listener with id: {0}'.format(listener_id)
        raise IndexError(err)

    def _new_schedule(self, raw_schedule):
        if raw_schedule['type'] == 'Election':
            return schedule.RainwaveElection(self, raw_schedule)
        if raw_schedule['type'] == 'OneUp':
            return schedule.RainwaveOneTimePlay(self, raw_schedule)

    def _stale(self):
        """Return True if timeline information (:attr:`schedule_current`,
        :attr:`schedule_next`, and :attr:`schedule_history`) is missing or out
        of date."""

        if len(self._sched_next) < 1:
            return True
        now = datetime.datetime.utcnow()
        ts = self._sched_current['end']
        ts = datetime.datetime.utcfromtimestamp(ts)
        return now > ts

    @property
    def albums(self):
        """A list of :class:`RainwaveAlbum` objects in the playlist of the
        channel."""

        if self._raw_albums is None:
            d = self.client.call('all_albums', {'sid': self.id})
            if 'all_albums' in d:
                self._raw_albums = d['all_albums']
        if self._albums is None:
            self._albums = []
            for raw_album in self._raw_albums:
                new_album = album.RainwaveAlbum(self, raw_album)
                self._albums.append(new_album)
        return self._albums

    @property
    def artists(self):
        """A list of :class:`RainwaveArtist` objects in the playlist of the
        channel."""

        if self._raw_artists is None:
            d = self.client.call('all_artists', {'sid': self.id})
            if 'all_artists' in d:
                self._raw_artists = d['all_artists']
        if self._artists is None:
            self._artists = []
            for raw_artist in self._raw_artists:
                new_artist = artist.RainwaveArtist(self, raw_artist)
                self._artists.append(new_artist)
        return self._artists

    def clear_rating(self, song_id):
        args = {'sid': self.id, 'song_id': song_id}
        return self.client.call('clear_rating', args)

    @property
    def client(self):
        """The :class:`RainwaveClient` object that the channel belongs to."""
        return self._client

    def delete_request(self, song_id):
        args = {'song_id': song_id, 'sid': self.id}
        d = self.client.call('delete_request', args)
        if d['delete_request_result']['success']:
            with self._requests_lock:
                self._raw_user_requests = d['requests']
            return d
        else:
            raise Exception(d['delete_request_result']['text'])

    @property
    def description(self):
        """A description of the channel."""
        return self['description']

    def fave_album(self, album_id, fave):
        args = {'album_id': album_id, 'fave': fave, 'sid': self.id}
        return self.client.call('fave_album', args)

    def fave_song(self, song_id, fave):
        args = {'song_id': song_id, 'fave': fave}
        return self.client.call('fave_song', args)

    def get_album_by_id(self, album_id):
        """Return a :class:`RainwaveAlbum` for the given album ID. Raise an
        :exc:`IndexError` if there is no album with the given ID in the
        playlist of the channel.

        :param album_id: the ID of the desired album.
        :type album_id: int
        """

        for alb in self.albums:
            if alb.id == album_id:
                args = {'sid': self.id, 'id': album_id}
                d = self.client.call('album', args)
                return album.RainwaveAlbum(self, d['album'])
        error = 'Channel does not contain album with id: {0}'.format(album_id)
        raise IndexError(error)

    def get_album_by_name(self, name):
        """Return a :class:`RainwaveAlbum` for the given album name. Raise an
        :exc:`IndexError` if there is no album with the given name in the
        playlist of the channel.

        :param name: the name of the desired album.
        :type name: str
        """

        for alb in self.albums:
            if alb.name == name:
                return alb
        error = 'Channel does not contain album with name: {0}'.format(name)
        raise IndexError(error)

    def get_artist_by_id(self, artist_id):
        """Return a :class:`RainwaveArtist` for the given artist ID. Raise an
        :exc:`IndexError` if there is no artist with the given ID in the
        playlist of the channel.

        :param artist_id: the ID of the desired artist.
        :type artist_id: int
        """

        args = {'sid': self.id, 'id': artist_id}
        d = self.client.call('artist', args)
        if 'id' in d['artist']:
            return artist.RainwaveArtist(self, d['artist'])
        err = 'Channel does not contain artist with id: {0}'.format(artist_id)
        raise IndexError(err)

    def get_listener_by_id(self, listener_id):
        """Return a :class:`RainwaveListener` for the given listener ID. Raise
        an :exc:`IndexError` if there is no listener with the given ID.

        :param listener_id: the ID of the desired listener.
        :type listener_id: int
        """

        raw_listener = self._get_listener_raw_info(listener_id)
        return listener.RainwaveListener(self, raw_listener)

    def get_listener_by_name(self, name):
        """Return a :class:`RainwaveListener` for the given listener name. Raise
        an :exc:`IndexError` if there is no listener with the given name
        currently listening to the channel.

        :param name: the name of the desired listener.
        :type name: str
        """

        for _listener in self.listeners:
            if _listener.name == name:
                return _listener
        err = 'No current listener named {0}'.format(name)
        raise IndexError(err)

    def get_song_by_id(self, song_id):
        """Return a :class:`RainwaveSong` for the given song ID. Raise an
        :exc:`IndexError` if there is no song with the given ID in the playlist
        of the channel.

        :param song_id: the ID of the desired song.
        :type song_id: int
        """

        args = {'sid': self.id, 'id': song_id}
        d = self.client.call('song', args)
        if 'albums' in d['song']:
            alb = self.get_album_by_id(d['song']['albums'][0]['id'])
            return song.RainwaveSong(alb, d['song'])
        err = 'Channel does not contain song with id: {0}'.format(song_id)
        raise IndexError(err)

    @property
    def id(self):
        """The ID of the channel."""
        return self['id']

    @property
    def listeners(self):
        """A list of :class:`RainwaveListener` objects listening to the
        channel."""
        _listeners = []
        d = self.client.call('current_listeners', {'sid': self.id})
        for raw_listener in d['current_listeners']:
            _listeners.append(listener.RainwaveListener(self, raw_listener))
        return _listeners

    @property
    def name(self):
        """The name of the channel."""
        return self['name']

    @property
    def ogg_stream(self):
        """The URL of the OGG stream for the channel. See also
        :attr:`mp3_stream`."""
        return self.mp3_stream.replace('.mp3', '.ogg')

    def rate(self, song_id, rating):
        args = {'sid': self.id, 'song_id': song_id, 'rating': rating}
        return self.client.call('rate', args)

    def reorder_requests(self, order):
        args = {'sid': self.id, 'order': order}
        d = self.client.call('order_requests', args)
        if d['order_requests_result']['success']:
            with self._requests_lock:
                self._raw_user_requests = d['requests']
            return d
        else:
            raise Exception(d['order_requests_result']['text'])

    def request_song(self, song_id):
        args = {'song_id': song_id, 'sid': self.id}
        d = self.client.call('request', args)
        if d['request_result']['success']:
            with self._requests_lock:
                self._raw_user_requests = d['requests']
            return d
        else:
            raise Exception(d['request_result']['text'])

    def clear_requests(self):
        return self.client.call('clear_requests', {'sid': self.id})

    @property
    def requests(self):
        """A list of :class:`RainwaveRequest` objects in the request line of
        the channel."""
        if self._stale():
            self._do_async_get()
        rqs = []
        with self._requests_lock:
            for raw_request in self._raw_requests:
                if raw_request.get('song_id') is None:
                    continue
                _song = self.get_song_by_id(raw_request['song_id'])
                _reqr = self.get_listener_by_id(raw_request['user_id'])
                rq = request.RainwaveRequest.request_from_song(_song, _reqr)
                rqs.append(rq)
        return rqs

    @property
    def schedule_current(self):
        """The current :class:`RainwaveSchedule` for the channel."""
        if self._stale():
            self._do_async_get()
        with self._sched_lock:
            sched_current = self._new_schedule(self._sched_current)
        return sched_current

    @property
    def schedule_history(self):
        """A list of the past :class:`RainwaveSchedule` objects for the
        channel."""
        if self._stale():
            self._do_async_get()
        sched_history = []
        with self._sched_lock:
            for raw_sched in self._sched_history:
                sched_history.append(self._new_schedule(raw_sched))
        return sched_history

    @property
    def schedule_next(self):
        """A list of the next :class:`RainwaveSchedule` objects for the
        channel."""
        if self._stale():
            self._do_async_get()
        sched_next = []
        with self._sched_lock:
            for raw_sched in self._sched_next:
                sched_next.append(self._new_schedule(raw_sched))
        return sched_next

    def start_sync(self):
        """Begin syncing the timeline for the channel."""

        self.stop_sync()
        self._sync_thread = threading.Thread(target=self._do_sync_thread)
        self._sync_thread.daemon = True
        self._sync_thread.start()

    def stop_sync(self):
        """Stop syncing the timeline for the channel."""

        self._do_sync = False
        self._sync_thread = None

    @property
    def mp3_stream(self):
        """The URL of the MP3 stream for the channel. See also
        :attr:`ogg_stream`."""
        return self['stream']

    @property
    def user_requests(self):
        """A :class:`RainwaveUserRequestQueue` of :class:`RainwaveUserRequest`
        objects in the listener's personal request queue."""
        if self._stale():
            self._do_async_get()
        rqs = request.RainwaveUserRequestQueue(self)
        with self._requests_lock:
            for raw_request in self._raw_user_requests:
                album_id = raw_request['albums'][0]['id']
                alb = self.get_album_by_id(album_id)
                rq = request.RainwaveUserRequest(alb, raw_request)
                rqs.append(rq)
        return rqs

    def vote(self, entry_id):
        args = {'entry_id': entry_id, 'sid': self.id}
        return self.client.call('vote', args)
