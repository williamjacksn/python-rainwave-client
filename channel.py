import threading

import album
import artist


class RainwaveChannel(object):

    simple_properties = [u'description', u'id', u'name', u'oggstream',
        u'stream']

    def __init__(self, client, raw_info):
        self._client = client
        self._raw_info = raw_info

    def __getattr__(self, name):
        if name in self.simple_properties:
            return self._raw_info[name]
        else:
            raise AttributeError

    @property
    def albums(self):
        if not hasattr(self, u'_raw_albums'):
            self._raw_albums = self._client.call(u'async/{}/all_albums'.format(self.id))
        if not hasattr(self, u'_albums'):
            self._albums = []
            for raw_album in self._raw_albums[u'playlist_all_albums']:
                new_album = album.RainwaveAlbum(self, raw_album)
                self._albums.append(new_album)
        return self._albums

    @property
    def artists(self):
        if not hasattr(self, u'_raw_artists'):
            self._raw_artists = self._client.call(u'async/{}/artist_list'.format(self.id))
        if not hasattr(self, u'_artists'):
            self._artists = []
            for raw_artist in self._raw_artists[u'artist_list']:
                new_artist = artist.RainwaveArtist(self, raw_artist)
                self._artists.append(new_artist)
        return self._artists

    def _do_sync_thread(self):
        self._do_sync = True
        while self._do_sync:
            if hasattr(self, u'_raw_timeline'):
                d = self._client.call(u'sync/{}/sync'.format(self.id))
            else:
                d = self._client.call(u'sync/{}/init'.format(self.id))
            if self._do_sync:
                self._raw_timeline = d

    def start_sync(self):
        self.stop_sync()
        self._sync_thread = threading.Thread(target=self._do_sync_thread)
        self._sync_thread.daemon = True
        self._sync_thread.start()

    def stop_sync(self):
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
        raw_artist = {}
        for artist in self.artists:
            if artist.id == artist_id:
                raw_artist = artist._raw_info
        args = {u'artist_id': artist_id}
        d = self._client.call(u'async/{}/artist_detail'.format(self.id), args)
        return dict(raw_artist.items() + d[u'artist_detail'].items())
