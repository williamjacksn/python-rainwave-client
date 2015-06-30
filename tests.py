from __future__ import unicode_literals

import datetime
import os
import rainwaveclient
import random
import sys
import unittest

if 'RW_USER_ID' in os.environ:
    USER_ID = int(os.environ.get('RW_USER_ID'))
else:
    sys.exit('Please set the {!r} environment variable'.format('RW_USER_ID'))

if 'RW_KEY' in os.environ:
    KEY = os.environ.get('RW_KEY')
else:
    sys.exit('Please set the {!r} environment variable'.format('RW_KEY'))


class TestRainwaveClient(unittest.TestCase):

    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)

    def test_str(self):
        _str = 'RainwaveClient(user_id={0}, key={1!r})'.format(USER_ID, KEY)
        self.assertEqual(str(self.rw), _str)

    def test_repr(self):
        _repr = 'RainwaveClient(user_id={0}, key={1!r})'.format(USER_ID, KEY)
        self.assertEqual(repr(self.rw), _repr)

    def test_base_url(self):
        self.assertEqual(self.rw.base_url, 'http://rainwave.cc/api4/')

    def test_art_fmt(self):
        self.assertEqual(self.rw.art_fmt, 'http://rainwave.cc{0}_320.jpg')

    def test_user_id(self):
        self.assertEqual(self.rw.user_id, USER_ID)

    def test_user_id_set(self):
        self.rw.user_id = USER_ID

    def test_key(self):
        self.assertEqual(self.rw.key, KEY)

    def test_key_set(self):
        self.rw.key = KEY

    def test_channel_count(self):
        self.assertEqual(len(self.rw.channels), 5)


class TestRainwaveChannel(unittest.TestCase):

    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    chan = rw.channels[4]

    def test_repr(self):
        self.assertEqual(repr(self.chan), '<RainwaveChannel [All]>')

    def test_str(self):
        _str = ('All: Video game music online radio, including remixes and '
                'original soundtracks!  Vote for the songs you want to hear!')
        self.assertEqual(str(self.chan), _str)

    def test_albums(self):
        self.assertTrue(len(self.chan.albums) > 1)

    def test_artists(self):
        self.assertTrue(len(self.chan.artists) > 1)

    def test_client(self):
        self.assertEqual(self.chan.client, self.rw)

    def test_delete_request(self):
        self.assertRaises(Exception, self.chan.delete_request, 1)

    def test_description(self):
        desc = ('Video game music online radio, including remixes and original '
                'soundtracks!  Vote for the songs you want to hear!')
        self.assertEqual(self.chan.description, desc)

    def test_get_album_by_id(self):
        self.assertRaises(IndexError, self.chan.get_album_by_id, 999999)
        alb = self.chan.get_album_by_id(3)
        self.assertEqual(alb.name, 'Goemon\'s Great Adventure')

    def test_get_album_by_name(self):
        self.assertRaises(IndexError, self.chan.get_album_by_name, 'Mega Ran')
        alb = self.chan.get_album_by_name('Goemon\'s Great Adventure')
        self.assertEqual(alb.id, 3)

    def test_get_artist_by_id(self):
        self.assertRaises(IndexError, self.chan.get_artist_by_id, 1)
        artist = self.chan.get_artist_by_id(1053)
        self.assertEqual(artist.name, 'TheGuitahHeroe')

    def test_get_listener_by_id(self):
        self.assertRaises(IndexError, self.chan.get_listener_by_id, 9999999)
        listener = self.chan.get_listener_by_id(2)
        self.assertEqual(listener.name, 'Rob')

    def test_get_listener_by_name(self):
        first_listener = self.chan.listeners[0]
        got = self.chan.get_listener_by_name(first_listener.name)
        self.assertEqual(got.id, first_listener.id)
        self.assertRaises(IndexError, self.chan.get_listener_by_name, '______')

    def test_get_song_by_id(self):
        self.assertRaises(IndexError, self.chan.get_song_by_id, 9999999)
        song = self.chan.get_song_by_id(8151)
        self.assertEqual(song.title, 'This Treasure')

    def test_id(self):
        self.assertEqual(self.chan.id, 5)

    def test_listeners(self):
        self.assertTrue(len(self.chan.listeners) > 1)

    def test_name(self):
        self.assertEqual(self.chan.name, 'All')

    def test_oggstream(self):
        stream = 'http://allstream.rainwave.cc:8000/all.ogg?' + str(USER_ID)
        self.assertTrue(self.chan.ogg_stream.startswith(stream))

    def test_reorder_requests(self):
        self.assertRaises(Exception, self.chan.reorder_requests, [])

    def test_request_song(self):
        self.assertRaises(Exception, self.chan.request_song, 999999)

    def test_requests(self):
        self.assertTrue(len(self.chan.requests) > 0)

    def test_schedule_current(self):
        title = self.chan.schedule_current.songs[0].title
        if sys.version_info[0] == 2:
            self.assertTrue(isinstance(title, unicode))
        else:
            self.assertTrue(isinstance(title, str))

    def test_schedule_history(self):
        title = self.chan.schedule_history[0].songs[0].title
        if sys.version_info[0] == 2:
            self.assertTrue(isinstance(title, unicode))
        else:
            self.assertTrue(isinstance(title, str))

    def test_schedule_next(self):
        title = self.chan.schedule_next[0].songs[0].title
        if sys.version_info[0] == 2:
            self.assertTrue(isinstance(title, unicode))
        else:
            self.assertTrue(isinstance(title, str))

    def test_stream(self):
        stream = 'http://allstream.rainwave.cc:8000/all.mp3?' + str(USER_ID)
        self.assertTrue(self.chan.mp3_stream.startswith(stream))

    def test_sync(self):
        self.chan.start_sync()
        self.chan.stop_sync()


class TestRainwaveAlbum(unittest.TestCase):

    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    alb = rw.channels[4].get_album_by_id(1)

    def test_added_on(self):
        self.assertTrue(isinstance(self.alb.added_on, datetime.datetime))

    def test_art(self):
        art = 'http://rainwave.cc/album_art/a_1_320.jpg'
        self.assertEqual(self.alb.art, art)

    def test_categories(self):
        self.assertTrue(len(self.alb.categories) > 0)

    def test_channel(self):
        self.assertEqual(self.alb.channel.id, 5)

    def test_cool(self):
        self.assertTrue(isinstance(self.alb.cool, bool))

    def test_cool_lowest(self):
        self.assertTrue(isinstance(self.alb.cool_lowest, datetime.datetime))

    def test_fave(self):
        self.assertFalse(self.alb.fave)

    def test_fave_count(self):
        self.assertTrue(self.alb.fave_count > 0)

    def test_fave_set(self):
        self.alb.fave = True
        self.assertTrue(self.alb.fave)
        self.alb.fave = False
        self.assertFalse(self.alb.fave)

    def test_gave_set_same(self):
        self.alb.fave = False
        self.assertFalse(self.alb.fave)

    def test_get_song_by_id(self):
        self.assertRaises(IndexError, self.alb.get_song_by_id, 100)
        song = self.alb.get_song_by_id(1)
        self.assertEqual(song.title, 'Conflict\'s Chime')

    def test_id(self):
        self.assertEqual(self.alb.id, 1)

    def test_name(self):
        self.assertEqual(self.alb.name, 'Bravely Default: Flying Fairy')

    def test_played_last(self):
        self.assertTrue(isinstance(self.alb.played_last, datetime.datetime))

    def test_rating(self):
        self.assertTrue(self.alb.rating > 0)

    def test_rating_avg(self):
        self.assertTrue(self.alb.rating_avg > 0)

    def test_rating_complete(self):
        self.assertTrue(isinstance(self.alb.rating_complete, bool))

    def test_rating_count(self):
        self.assertTrue(self.alb.rating_count > 0)

    def test_rating_histogram(self):
        self.assertTrue(isinstance(self.alb.rating_histogram, dict))

    def test_rating_rank(self):
        self.assertTrue(self.alb.rating_rank > 0)

    def test_rating_user(self):
        self.assertEqual(self.alb.rating_user, self.alb.rating)

    def test_repr(self):
        _repr = '<RainwaveAlbum [All // Bravely Default: Flying Fairy]>'
        self.assertEqual(repr(self.alb), _repr)

    def test_request_count(self):
        self.assertTrue(self.alb.request_count > 0)

    def test_request_rank(self):
        self.assertTrue(self.alb.request_rank > 0)

    def test_songs(self):
        self.assertTrue(len(self.alb.songs) > 0)

    def test_str(self):
        self.assertEqual(str(self.alb), 'All // Bravely Default: Flying Fairy')

    def test_vote_count(self):
        self.assertTrue(self.alb.vote_count > 0)


class TestRainwaveSong(unittest.TestCase):

    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    song = rw.channels[4].get_song_by_id(1)

    def test_album(self):
        self.assertEqual(self.song.album.name, 'Bravely Default: Flying Fairy')

    def test_artist_string(self):
        self.assertEqual(self.song.artist_string, 'Revo')

    def test_artists(self):
        self.assertEqual(len(self.song.artists), 1)

    def test_available(self):
        self.assertTrue(isinstance(self.song.available, bool))

    def test_avail_is_not_cool(self):
        self.assertTrue(self.song.available != self.song.cool)

    def test_categories(self):
        self.assertTrue(len(self.song.categories) > 0)

    def test_channel_id(self):
        self.assertEqual(self.song.channel_id, 5)

    def test_cool(self):
        self.assertTrue(isinstance(self.song.cool, bool))

    def test_fave(self):
        self.assertFalse(self.song.fave)

    def test_fave_set(self):
        self.song.fave = True
        self.assertTrue(self.song.fave)
        self.song.fave = False
        self.assertFalse(self.song.fave)

    def test_fave_set_same(self):
        self.song.fave = False

    def test_id(self):
        self.assertEqual(self.song.id, 1)

    def test_len(self):
        self.assertEqual(len(self.song), 167)

    def test_length(self):
        self.assertEqual(self.song.length, 167)

    def test_link_text(self):
        self.assertEqual(self.song.link_text, 'Click for More Info')

    def test_origin_channel_id(self):
        self.assertEqual(self.song.origin_channel_id, 1)

    def test_origin_sid(self):
        self.assertEqual(self.song.origin_sid, 1)

    def test_rating(self):
        self.assertTrue(self.song.rating > 0)

    def test_rating_set(self):
        self.song.rating = 5
        self.assertEqual(self.song.rating, 5)
        self.song.rating = 3

    def test_rating_set_invalid(self):
        def bad_rate():
            self.song.rating = 6
        self.assertRaises(Exception, bad_rate)

    def test_rating_set_same(self):
        self.song.rating = 3

    def test_rating_delete(self):
        del self.song.rating
        self.assertTrue(self.song.rating is None)
        self.song.rating = 3

    def test_rating_allowed(self):
        self.assertTrue(isinstance(self.song.rating_allowed, bool))

    def test_rating_avg(self):
        self.assertTrue(self.song.rating_avg > 0)

    def test_rating_count(self):
        self.assertTrue(self.song.rating_count > 0)

    def test_rating_histogram(self):
        self.assertTrue(isinstance(self.song.rating_histogram, dict))

    def test_rating_rank(self):
        self.assertTrue(self.song.rating_rank > 0)

    def test_rating_user(self):
        self.assertEqual(self.song.rating_user, self.song.rating)

    def test_repr(self):
        _repr = ('<RainwaveSong [All // Bravely Default: Flying Fairy // '
                 'Conflict\'s Chime // Revo]>')
        self.assertEqual(repr(self.song), _repr)

    def test_request_count(self):
        self.assertTrue(self.song.request_count > 0)

    def test_request_rank(self):
        self.assertTrue(self.song.request_rank > 0)

    def test_sid(self):
        self.assertEqual(self.song.sid, 5)

    def test_str(self):
        _str = ('All // Bravely Default: Flying Fairy // Conflict\'s Chime // '
                'Revo')
        self.assertEqual(str(self.song), _str)

    def test_title(self):
        self.assertEqual(self.song.title, 'Conflict\'s Chime')

    def test_url(self):
        self.assertEqual(self.song.url, 'http://vgmdb.net/album/33726')


class TestRainwaveArtist(unittest.TestCase):

    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    a = rw.channels[4].get_artist_by_id(288)

    def test_channel(self):
        self.assertEqual(self.a.channel, self.rw.channels[4])

    def test_id(self):
        self.assertEqual(self.a.id, 288)

    def test_name(self):
        self.assertEqual(self.a.name, 'Stephane Bellanger')

    def test_repr(self):
        self.assertEqual(repr(self.a), '<RainwaveArtist [Stephane Bellanger]>')

    def test_song_count(self):
        self.assertEqual(self.a.song_count, 9)

    def test_songs(self):
        self.assertTrue(isinstance(self.a.songs, list))
        self.assertTrue(len(self.a.songs) > 0)

    def test_str(self):
        self.assertEqual(str(self.a), 'Stephane Bellanger')


class TestRainwaveListener(unittest.TestCase):

    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    l = rw.channels[4].get_listener_by_id(5049)

    def test_avatar(self):
        _avatar = ('http://rainwave.cc/forums/download/file.php?'
                   'avatar=5049_1408449931.jpg')
        self.assertEqual(self.l.avatar, _avatar)

    def test_color(self):
        self.assertEqual(self.l.color, 'FF0000')

    def test_colour(self):
        self.assertEqual(self.l.colour, 'FF0000')

    def test_id(self):
        self.assertEqual(self.l.id, 5049)

    def test_losing_requests(self):
        self.assertTrue(self.l.losing_requests > 0)

    def test_losing_votes(self):
        self.assertTrue(self.l.losing_votes > 0)

    def test_mind_changes(self):
        self.assertTrue(self.l.mind_changes > 0)

    def test_name(self):
        self.assertEqual(self.l.name, 'William')

    def test_rank(self):
        self.assertEqual(self.l.rank, 'Mister Three')

    def test_repr(self):
        self.assertEqual(repr(self.l), '<RainwaveListener [William]>')

    def test_str(self):
        self.assertEqual(str(self.l), 'William')

    def test_total_ratings(self):
        self.assertTrue(self.l.total_ratings > 0)

    def test_total_requests(self):
        self.assertTrue(self.l.total_requests > 0)

    def test_total_votes(self):
        self.assertTrue(self.l.total_votes > 0)

    def test_user_id(self):
        self.assertEqual(self.l.user_id, 5049)

    def test_winning_requests(self):
        self.assertTrue(self.l.winning_requests > 0)

    def test_winning_votes(self):
        self.assertTrue(self.l.winning_votes > 0)


class TestRainwaveRequest(unittest.TestCase):

    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    rq = rw.channels[4].requests[0]

    def test_repr(self):
        self.assertTrue(repr(self.rq).startswith('<RainwaveRequest '))

    def test_requester(self):
        if sys.version_info[0] == 2:
            self.assertTrue(isinstance(self.rq.requester.name, unicode))
        else:
            self.assertTrue(isinstance(self.rq.requester.name, str))


class TestRainwaveCandidate(unittest.TestCase):

    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    cand = rw.channels[4].schedule_next[0].candidates[0]

    def test_repr(self):
        self.assertTrue(repr(self.cand).startswith('<RainwaveCandidate '))

    def test_entry_id(self):
        self.assertTrue(self.cand.entry_id > 0)

    def test_is_request(self):
        self.assertTrue(isinstance(self.cand.is_request, bool))

    def test_requested_by(self):
        if self.cand.is_request:
            name = self.cand.requested_by.name
            if sys.version_info[0] == 2:
                self.assertTrue(isinstance(name, unicode))
            else:
                self.assertTrue(isinstance(name, str))
        else:
            self.assertTrue(self.cand.requested_by is None)

    def test_vote(self):
        self.cand.vote()


class TestRainwaveUserRequest(unittest.TestCase):

    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    urq = rw.channels[4].user_requests

    def test_repr(self):
        self.assertTrue(repr(self.urq[0]).startswith('<RainwaveUserRequest'))

    def test_urq_len(self):
        self.assertTrue(len(self.urq) > 0)

    def test_urq_reorder(self):
        self.assertRaises(Exception, self.urq.reorder, [99])
        self.assertRaises(Exception, self.urq.reorder, [98, 99])
        indices = list(range(len(self.urq)))
        random.shuffle(indices)
        self.urq.reorder(indices)

    def test_request_delete(self):
        song = self.rw.channels[4].albums[0].songs[0]
        song.request()
        for ur in self.rw.channels[4].user_requests:
            if ur.id == song.id:
                ur.delete()

    def test_blocked(self):
        self.assertTrue(self.urq[0].blocked)


class TestRainwaveSchedule(unittest.TestCase):

    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)

    def test_id(self):
        event = self.rw.channels[4].schedule_current
        self.assertTrue(isinstance(event.id, int))

    def test_repr(self):
        event = self.rw.channels[4].schedule_current
        self.assertTrue(repr(event).startswith('<Rainwave'))

    def test_start(self):
        event = self.rw.channels[4].schedule_current
        self.assertTrue(isinstance(event.start, datetime.datetime))

if __name__ == '__main__':
    unittest.main()
