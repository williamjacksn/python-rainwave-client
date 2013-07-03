import threading

import album
import artist
import dispatch
import schedule

pre_sync = dispatch.Signal()
post_sync = dispatch.Signal()


class RainwaveChannel(object):
    '''A :class:`RainwaveChannel` object represents one channel on the Rainwave
    network.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveClient.channels`.

    :param client: the :class:`RainwaveClient` parent object.
    :param raw_info: a dictionary of information provided by the API that
        describes the channel.
    '''

    def __init__(self, client, raw_info):
        self._client = client
        self._raw_info = raw_info

    def __repr__(self):
        return u'RainwaveChannel({})'.format(self.name)

    def __str__(self):
        return u'{}, {}'.format(self.name, self.description)

    @property
    def albums(self):
        '''A list of :class:`RainwaveAlbum` objects in the playlist of the
        channel.'''

        if not hasattr(self, u'_raw_albums'):
            path = u'async/{}/all_albums'.format(self.id)
            self._raw_albums = self._client.call(path)
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
            self._raw_artists = self._client.call(path)
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
    def id(self):
        '''The ID of the channel.'''
        return self._raw_info[u'id']

    @property
    def name(self):
        '''The name of the channel.'''
        return self._raw_info[u'name']

    @property
    def oggstream(self):
        '''The URL of the OGG stream for the channel.'''
        return self._raw_info[u'oggstream']

    @property
    def stream(self):
        '''The URL of the MP3 stream for the channel.'''
        return self._raw_info[u'stream']

    @property
    def schedule_current(self):
        '''The current :class:`RainwaveSchedule` for the channel.'''
        if not hasattr(self, '_schedule_current'):
            self._do_async_get()
        return self._schedule_current
    
    @property
    def schedule_history(self):
        '''A list of the past :class:`RainwaveSchedule` objects for the channel.'''
        if not hasattr(self, '_schedule_history'):
            self._do_async_get()
        return self._schedule_history
    
    @property
    def schedule_next(self):
        '''A list of the next :class:`RainwaveSchedule` objects for the channel.'''
        if not hasattr(self, '_schedule_next'):
            self._do_async_get()
        return self._schedule_next

    def _do_async_get(self):
        d = self._client.call(u'/async/{}/get'.format(self.id))
        self._cache_raw_timeline(d)

    def _do_sync_thread(self):
        self._do_sync = True
        while self._do_sync:
            pre_sync.send(self)
            if hasattr(self, u'_raw_timeline'):
                d = self._client.call(u'sync/{}/sync'.format(self.id))
            else:
                d = self._client.call(u'sync/{}/init'.format(self.id))
            if self._do_sync:
                self._cache_raw_timeline(d)
                post_sync.send(self, channel=self)

    def _cache_raw_timeline(self, raw_timeline):
        def new_schedule(raw_sched):
            return schedule.RainwaveSchedule(self._client, self, raw_sched)
        self._raw_timeline = raw_timeline
        self._schedule_current = new_schedule(raw_timeline[u'sched_current'])
        self._schedule_next = []
        self._schedule_history = []
        for raw_sched in raw_timeline[u'sched_next']:
            self._schedule_next.append(new_schedule(raw_sched))
        for raw_sched in raw_timeline[u'sched_history']:
            self._schedule_history.append(new_schedule(raw_sched))

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

    def _get_album_raw_info(self, album_id):
        args = {u'album_id': album_id}
        d = self._client.call(u'async/{}/album'.format(self.id), args)
        return d[u'playlist_album']

    def _get_artist_raw_info(self, artist_id):
        raw_info = {}
        for artist in self.artists:
            if artist.id == artist_id:
                raw_info = artist._raw_info
        args = {u'artist_id': artist_id}
        d = self._client.call(u'async/{}/artist_detail'.format(self.id), args)
        return dict(raw_info.items() + d[u'artist_detail'].items())
