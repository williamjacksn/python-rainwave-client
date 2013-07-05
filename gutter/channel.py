import album
import artist
import dispatch
import listener
import schedule
import threading

pre_sync = dispatch.Signal()
post_sync = dispatch.Signal()


class RainwaveChannel(object):
    '''A :class:`RainwaveChannel` object represents one channel on the Rainwave
    network.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveClient.channels`.
    '''

    #: The :class:`RainwaveClient` object that belongs to the channel.
    client = None

    def __init__(self, client, raw_info):
        self.client = client
        self._raw_info = raw_info
        self._do_sync = False

    def __repr__(self):
        return '<RainwaveChannel [{}]>'.format(self.name)

    def __str__(self):
        return '{}, {}'.format(self.name, self.description)

    def _do_async_get(self):
        d = self.client.call(u'/async/{}/get'.format(self.id))
        self._raw_timeline = d

    def _do_sync_thread(self):
        self._do_sync = True
        while self._do_sync:
            pre_sync.send(self)
            if hasattr(self, u'_raw_timeline'):
                d = self.client.call(u'sync/{}/sync'.format(self.id))
            else:
                d = self.client.call(u'sync/{}/init'.format(self.id))
            if self._do_sync:
                self._raw_timeline = d
                post_sync.send(self, channel=self)

    def _get_album_raw_info(self, album_id):
        args = {u'album_id': album_id}
        d = self.client.call(u'async/{}/album'.format(self.id), args)
        return d[u'playlist_album']

    def _get_artist_raw_info(self, artist_id):
        raw_info = {}
        for artist in self.artists:
            if artist.id == artist_id:
                raw_info = artist._raw_info
        args = {u'artist_id': artist_id}
        d = self.client.call(u'async/{}/artist_detail'.format(self.id), args)
        return dict(raw_info.items() + d[u'artist_detail'].items())

    def _get_listener_raw_info(self, listener_id):
        args = {u'listener_uid': listener_id}
        d = self.client.call(u'async/{}/listener_detail'.format(self.id), args)
        return d[u'listener_detail']

    def _new_schedule(self, raw_schedule):
        if raw_schedule[u'sched_type'] == 0:
            return schedule.RainwaveElection(self, raw_schedule)

    @property
    def albums(self):
        '''A list of :class:`RainwaveAlbum` objects in the playlist of the
        channel.'''

        if not hasattr(self, u'_raw_albums'):
            path = u'async/{}/all_albums'.format(self.id)
            self._raw_albums = self.client.call(path)
        if not hasattr(self, u'_albums'):
            self._albums = []
            for raw_album in self._raw_albums[u'playlist_all_albums']:
                new_album = album.RainwaveAlbum(self, raw_album)
                self._albums.append(new_album)
        return self._albums

    @property
    def artists(self):
        '''A list of :class:`RainwaveArtist` objects in the playlist of the
        channel.'''

        if not hasattr(self, u'_raw_artists'):
            path = u'async/{}/artist_list'.format(self.id)
            self._raw_artists = self.client.call(path)
        if not hasattr(self, u'_artists'):
            self._artists = []
            for raw_artist in self._raw_artists[u'artist_list']:
                new_artist = artist.RainwaveArtist(self, raw_artist)
                self._artists.append(new_artist)
        return self._artists

    @property
    def description(self):
        '''A description of the channel.'''
        return self._raw_info[u'description']

    @property
    def guest_count(self):
        '''The number of guests listening to the channel.'''
        d = self.client.call(u'async/{}/listeners_current'.format(self.id))
        return d[u'listeners_current'][u'guests']

    @property
    def id(self):
        '''The ID of the channel.'''
        return self._raw_info[u'id']

    @property
    def listeners(self):
        '''A list of :class:`RainwaveListener` objects listening to the
        channel.'''
        _listeners = []
        d = self.client.call(u'async/{}/listeners_current'.format(self.id))
        for raw_listener in d[u'listeners_current'][u'users']:
            _listeners.append(listener.RainwaveListener(self, raw_listener))
        return _listeners

    @property
    def name(self):
        '''The name of the channel.'''
        return self._raw_info[u'name']

    @property
    def oggstream(self):
        '''The URL of the OGG stream for the channel.'''
        return self._raw_info[u'oggstream']

    @property
    def schedule_current(self):
        '''The current :class:`RainwaveSchedule` for the channel.'''
        if not self._do_sync:
            self._do_async_get()
        return self._new_schedule(self._raw_timeline[u'sched_current'])

    @property
    def schedule_history(self):
        '''A list of the past :class:`RainwaveSchedule` objects for the
        channel.'''
        if not self._do_sync:
            self._do_async_get()
        sched_history = []
        for raw_sched in self._raw_timeline[u'sched_history']:
            sched_history.append(self._new_schedule(raw_sched))
        return sched_history

    @property
    def schedule_next(self):
        '''A list of the next :class:`RainwaveSchedule` objects for the
        channel.'''
        if not self._do_sync:
            self._do_async_get()
        sched_next = []
        for raw_sched in self._raw_timeline[u'sched_next']:
            sched_next.append(self._new_schedule(raw_sched))
        return sched_next

    @property
    def stream(self):
        '''The URL of the MP3 stream for the channel.'''
        return self._raw_info[u'stream']

    def get_album_by_id(self, id):
        '''Returns a :class:`RainwaveAlbum` for the given album ID. Raises an
        :exc:`IndexError` if there is no album with the given ID in the
        playlist of the channel.

        :param id: the ID of the desired album.
        :type id: int
        '''

        for album in self.albums:
            if album.id == id:
                return album
        error = u'Channel does not contain album with id: {}'.format(id)
        raise IndexError(error)

    def get_album_by_name(self, name):
        '''Returns a :class:`RainwaveAlbum` for the given album name. Raises an
        :exc:`IndexError` if there is no album with the given ID in the
        playlist of the channel.

        :param name: the name of the desired album.
        :type name: str
        '''

        for album in self.albums:
            if album.name == name:
                return album
        error = u'Channel does not contain album with name: {}'.format(name)
        raise IndexError(error)

    def get_artist_by_id(self, id):
        '''Returns a :class:`RainwaveArtist` for the given artist ID. Raises an
        :exc:`IndexError` if there is no artist with the given ID in the
        playlist of the channel.

        :param id: the ID of the desired artist.
        :type id: int
        '''

        for artist in self.artists:
            if artist.id == id:
                return artist
        error = u'Channel does not contain artist with id: {}'.format(id)
        raise IndexError(error)

    def get_listener_by_name(self, name):
        '''Returns a :class:`RainwaveListener` for the given listener name.
        Raises an :exc:`IndexError` if there is no listener with the given name
        currently listening to the channel.

        :param name: the name of the desired listener.
        :type name: str
        '''

        for listener in self.listeners:
            if listener.name == name:
                return listener
        error = u'No current listener named {}'.format(name)
        raise IndexError(error)

    def rate_song(self, song_id, rating):
        args = {u'song_id': song_id, u'rating': rating}
        return self.client.call(u'async/{}/rate'.format(self.id), args)

    def start_sync(self):
        '''Begin syncing the timeline for the channel.'''

        self.stop_sync()
        self._sync_thread = threading.Thread(target=self._do_sync_thread)
        self._sync_thread.daemon = True
        self._sync_thread.start()

    def stop_sync(self):
        '''Stop syncing the timeline for the channel.'''

        self._do_sync = False
        if hasattr(self, u'_sync_thread'):
            del self._sync_thread
        if hasattr(self, u'_raw_timeline'):
            del self._raw_timeline
