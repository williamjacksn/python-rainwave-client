import threading

import album
import artist


class RainwaveChannel(object):
    '''A :class:`RainwaveChannel` object represents one channel on the Rainwave
    network.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveClient.channels`.

    :param client: the :class:`RainwaveClient` parent object.
    :param raw_info: a dictionary of information provided by the API that
        describes this channel.
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
        '''A list of :class:`RainwaveAlbum` objects in the playlist of this
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
        '''A list of :class:`RainwaveArtist` objects in the playlist of this
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

    def _do_sync_thread(self):
        self._do_sync = True
        while self._do_sync:
            if hasattr(self, u'_raw_timeline'):
                d = self._client.call(u'sync/{}/sync'.format(self.id))
            else:
                d = self._client.call(u'sync/{}/init'.format(self.id))
            if self._do_sync:
                self._raw_timeline = d

    def get_album_by_id(self, id):
        '''Returns a :class:`RainwaveAlbum` for the given album ID. Raises an
        :exc:`IndexError` if there is no album with the given ID in the
        playlist of this channel.

        :param id: ID of the desired album.
        :type id: int
        '''

        for album in self.albums:
            if album.id == id:
                return album
        error = u'Channel does not contain album with id: {}'.format(id)
        raise IndexError(error)

    def start_sync(self):
        '''Begin syncing the timeline for this channel.'''

        self.stop_sync()
        self._sync_thread = threading.Thread(target=self._do_sync_thread)
        self._sync_thread.daemon = True
        self._sync_thread.start()

    def stop_sync(self):
        '''Stop syncing the timeline for this channel.'''

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
