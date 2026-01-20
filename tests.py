import datetime
import logging
import os
import random
import secrets
import sys
import unittest

import notch

from src import rainwaveclient

log = logging.getLogger(__name__)


if "RW_USER_ID" in os.environ:
    USER_ID = int(os.environ["RW_USER_ID"])
else:
    sys.exit("Please set the RW_USER_ID environment variable")

if "RW_KEY" in os.environ:
    KEY = os.getenv("RW_KEY")
else:
    sys.exit("Please set the RW_KEY environment variable")


class TestRainwaveClient(unittest.TestCase):
    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)

    def test_str(self) -> None:
        _str = f"RainwaveClient(user_id={USER_ID}, key={KEY!r})"
        self.assertEqual(str(self.rw), _str)

    def test_repr(self) -> None:
        _repr = f"RainwaveClient(user_id={USER_ID}, key={KEY!r})"
        self.assertEqual(repr(self.rw), _repr)

    def test_base_url(self) -> None:
        self.assertEqual(self.rw.base_url, "https://rainwave.cc/api4/")

    def test_art_fmt(self) -> None:
        self.assertEqual(self.rw.art_fmt, "https://rainwave.cc{0}_320.jpg")

    def test_user_id(self) -> None:
        self.assertEqual(self.rw.user_id, USER_ID)

    def test_user_id_set(self) -> None:
        self.rw.user_id = USER_ID

    def test_key(self) -> None:
        self.assertEqual(self.rw.key, KEY)

    def test_key_set(self) -> None:
        self.rw.key = KEY

    def test_channel_count(self) -> None:
        self.assertEqual(len(self.rw.channels), 5)


class TestRainwaveChannel(unittest.TestCase):
    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    chan = rw.channels[4]

    def test_repr(self) -> None:
        self.assertEqual(repr(self.chan), "<RainwaveChannel [All]>")

    def test_str(self) -> None:
        _str = (
            "All: Video game music online radio, including remixes and "
            "original soundtracks!  Vote for the songs you want to hear!"
        )
        self.assertEqual(str(self.chan), _str)

    def test_albums(self) -> None:
        self.assertTrue(len(self.chan.albums) > 1)

    def test_artists(self) -> None:
        self.assertTrue(len(self.chan.artists) > 1)

    def test_client(self) -> None:
        self.assertEqual(self.chan.client, self.rw)

    def test_delete_request(self) -> None:
        self.assertRaises(Exception, self.chan.delete_request, 1)

    def test_description(self) -> None:
        desc = (
            "Video game music online radio, including remixes and original "
            "soundtracks!  Vote for the songs you want to hear!"
        )
        self.assertEqual(self.chan.description, desc)

    def test_get_album_by_id(self) -> None:
        self.assertRaises(IndexError, self.chan.get_album_by_id, 999999)
        alb = self.chan.get_album_by_id(3324)
        self.assertEqual(alb.name, "2")

    def test_get_album_by_name(self) -> None:
        self.assertRaises(IndexError, self.chan.get_album_by_name, "Mega Ran")
        alb = self.chan.get_album_by_name("2")
        self.assertEqual(alb.id, 3324)

    def test_get_artist_by_id(self) -> None:
        self.assertRaises(IndexError, self.chan.get_artist_by_id, 1)
        artist = self.chan.get_artist_by_id(22844)
        self.assertEqual(artist.name, "Shigeru Miyamoto")

    def test_get_listener_by_id(self) -> None:
        self.assertRaises(IndexError, self.chan.get_listener_by_id, 9999999)
        listener = self.chan.get_listener_by_id(2)
        self.assertEqual(listener.name, "rmcauley")

    def test_get_listener_by_name(self) -> None:
        first_listener = self.chan.listeners[0]
        got = self.chan.get_listener_by_name(first_listener.name)
        self.assertEqual(got.id, first_listener.id)
        self.assertRaises(IndexError, self.chan.get_listener_by_name, "______")

    def test_get_song_by_id(self) -> None:
        self.assertRaises(IndexError, self.chan.get_song_by_id, 9999999)
        song = self.chan.get_song_by_id(8151)
        self.assertEqual(song.title, "This Treasure")

    def test_id(self) -> None:
        self.assertEqual(self.chan.id, 5)

    def test_listeners(self) -> None:
        self.assertTrue(len(self.chan.listeners) > 1)

    def test_name(self) -> None:
        self.assertEqual(self.chan.name, "All")

    def test_ogg_stream(self) -> None:
        stream = f"http://allrelays.rainwave.cc/all.ogg?{USER_ID}"
        self.assertTrue(self.chan.ogg_stream.startswith(stream))

    def test_reorder_requests(self) -> None:
        self.assertRaises(Exception, self.chan.reorder_requests, [])

    def test_request_song(self) -> None:
        self.assertRaises(Exception, self.chan.request_song, 999999)

    def test_requests(self) -> None:
        self.assertTrue(len(self.chan.requests) > 0)

    def test_schedule_current(self) -> None:
        title = self.chan.schedule_current.songs[0].title
        self.assertIsInstance(title, str)

    def test_schedule_history(self) -> None:
        title = self.chan.schedule_history[0].songs[0].title
        self.assertIsInstance(title, str)

    def test_schedule_next(self) -> None:
        title = self.chan.schedule_next[0].songs[0].title
        self.assertIsInstance(title, str)

    def test_stream(self) -> None:
        stream = f"http://allrelays.rainwave.cc/all.mp3?{USER_ID}"
        self.assertTrue(self.chan.mp3_stream.startswith(stream))

    def test_sync(self) -> None:
        self.chan.start_sync()
        self.chan.stop_sync()


class TestRainwaveAlbum(unittest.TestCase):
    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    album_index: int = secrets.randbelow(100)
    alb = rw.channels[4].albums[album_index]

    def test_added_on(self) -> None:
        self.assertIsInstance(self.alb.added_on, datetime.datetime)

    def test_art(self) -> None:
        art = f"https://rainwave.cc/album_art/5_{self.alb.id}_320.jpg"
        self.assertEqual(self.alb.art, art)

    def test_categories(self) -> None:
        self.assertTrue(len(self.alb.categories) > 0)

    def test_channel(self) -> None:
        self.assertEqual(self.alb.channel.id, 5)

    def test_cool(self) -> None:
        self.assertIsInstance(self.alb.cool, bool)

    def test_cool_lowest(self) -> None:
        self.assertIsInstance(self.alb.cool_lowest, datetime.datetime)

    def test_fave(self) -> None:
        self.assertFalse(self.alb.fave)

    def test_fave_count(self) -> None:
        self.assertTrue(self.alb.fave_count > 0)

    def test_fave_set(self) -> None:
        self.alb.fave = True
        self.assertTrue(self.alb.fave)
        self.alb.fave = False
        self.assertFalse(self.alb.fave)

    def test_fave_set_same(self) -> None:
        self.alb.fave = False
        self.assertFalse(self.alb.fave)

    def test_get_song_by_id(self) -> None:
        self.assertRaises(IndexError, self.alb.get_song_by_id, 100)
        song = self.alb.songs[0]
        self.assertIsInstance(song.title, str)

    def test_id(self) -> None:
        self.assertIsInstance(self.alb.id, int)

    def test_name(self) -> None:
        self.assertIsInstance(self.alb.name, str)

    def test_played_last(self) -> None:
        self.assertIsInstance(self.alb.played_last, datetime.datetime)

    @unittest.skip("Still not sure why this is not working.")
    def test_rating(self) -> None:
        self.assertTrue(self.alb.rating > 0)

    def test_rating_avg(self) -> None:
        self.assertTrue(self.alb.rating_avg > 0)

    def test_rating_complete(self) -> None:
        self.assertIsInstance(self.alb.rating_complete, bool)

    def test_rating_count(self) -> None:
        self.assertTrue(self.alb.rating_count > 0)

    def test_rating_histogram(self) -> None:
        self.assertIsInstance(self.alb.rating_histogram, dict)

    def test_rating_rank(self) -> None:
        self.assertTrue(self.alb.rating_rank > 0)

    def test_rating_user(self) -> None:
        self.assertEqual(self.alb.rating_user, self.alb.rating)

    def test_repr(self) -> None:
        self.assertIsInstance(repr(self.alb), str)

    def test_request_count(self) -> None:
        self.assertTrue(self.alb.request_count > 0)

    def test_request_rank(self) -> None:
        self.assertTrue(self.alb.request_rank > 0)

    def test_songs(self) -> None:
        self.assertTrue(len(self.alb.songs) > 0)

    def test_str(self) -> None:
        self.assertIsInstance(str(self.alb), str)

    def test_vote_count(self) -> None:
        self.assertTrue(self.alb.vote_count > 0)


class TestRainwaveSong(unittest.TestCase):
    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    song = rw.channels[4].get_song_by_id(68)

    def test_album(self) -> None:
        self.assertEqual(self.song.album.name, "Puzzlejuice")

    def test_artist_string(self) -> None:
        self.assertEqual(self.song.artist_string, "Big Giant Circles")

    def test_artists(self) -> None:
        self.assertEqual(len(self.song.artists), 1)

    def test_available(self) -> None:
        self.assertIsInstance(self.song.available, bool)

    def test_avail_is_not_cool(self) -> None:
        self.assertTrue(self.song.available != self.song.cool)

    def test_categories(self) -> None:
        self.assertTrue(len(self.song.categories) > 0)

    def test_channel_id(self) -> None:
        self.assertEqual(self.song.channel_id, 5)

    def test_cool(self) -> None:
        self.assertIsInstance(self.song.cool, bool)

    def test_fave(self) -> None:
        self.assertFalse(self.song.fave)

    def test_fave_set(self) -> None:
        self.song.fave = True
        self.assertTrue(self.song.fave)
        self.song.fave = False
        self.assertFalse(self.song.fave)

    def test_fave_set_same(self) -> None:
        self.song.fave = False

    def test_id(self) -> None:
        self.assertEqual(self.song.id, 68)

    def test_len(self) -> None:
        self.assertEqual(len(self.song), 203)

    def test_length(self) -> None:
        self.assertEqual(self.song.length, 203)

    def test_link_text(self) -> None:
        self.assertEqual(self.song.link_text, "Get @ Bandcamp")

    def test_origin_channel_id(self) -> None:
        self.assertEqual(self.song.origin_channel_id, 1)

    def test_origin_sid(self) -> None:
        self.assertEqual(self.song.origin_sid, 1)

    def test_rating(self) -> None:
        self.assertTrue(self.song.rating > 0)

    def test_rating_set(self) -> None:
        self.song.rating = 5
        self.assertEqual(self.song.rating, 5)
        self.song.rating = 3

    def test_rating_set_invalid(self) -> None:
        def bad_rate() -> None:
            self.song.rating = 6

        self.assertRaises(Exception, bad_rate)

    def test_rating_set_same(self) -> None:
        self.song.rating = 3

    def test_rating_delete(self) -> None:
        del self.song.rating
        self.assertTrue(self.song.rating is None)
        self.song.rating = 3

    def test_rating_allowed(self) -> None:
        self.assertIsInstance(self.song.rating_allowed, bool)

    def test_rating_avg(self) -> None:
        self.assertTrue(self.song.rating_avg > 0)

    def test_rating_count(self) -> None:
        self.assertTrue(self.song.rating_count > 0)

    def test_rating_histogram(self) -> None:
        self.assertIsInstance(self.song.rating_histogram, dict)

    def test_rating_rank(self) -> None:
        self.assertTrue(self.song.rating_rank > 0)

    def test_rating_user(self) -> None:
        self.assertEqual(self.song.rating_user, self.song.rating)

    def test_repr(self) -> None:
        _repr = (
            "<RainwaveSong [All // Puzzlejuice // Sipping Juice // Big Giant Circles]>"
        )
        self.assertEqual(repr(self.song), _repr)

    def test_request_count(self) -> None:
        self.assertTrue(self.song.request_count > 0)

    def test_request_rank(self) -> None:
        self.assertTrue(self.song.request_rank > 0)

    def test_sid(self) -> None:
        self.assertEqual(self.song.sid, 5)

    def test_str(self) -> None:
        _str = "All // Puzzlejuice // Sipping Juice // Big Giant Circles"
        self.assertEqual(str(self.song), _str)

    def test_title(self) -> None:
        self.assertEqual(self.song.title, "Sipping Juice")

    def test_url(self) -> None:
        self.assertEqual(
            self.song.url,
            "https://biggiantcircles.bandcamp.com/album/puzzlejuice-soundtrack",
        )


class TestRainwaveArtist(unittest.TestCase):
    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    a = rw.channels[4].get_artist_by_id(288)

    def test_channel(self) -> None:
        self.assertEqual(self.a.channel, self.rw.channels[4])

    def test_id(self) -> None:
        self.assertEqual(self.a.id, 288)

    def test_name(self) -> None:
        self.assertEqual(self.a.name, "Stephane Bellanger")

    def test_repr(self) -> None:
        self.assertEqual(repr(self.a), "<RainwaveArtist [Stephane Bellanger]>")

    def test_song_count(self) -> None:
        self.assertEqual(self.a.song_count, 12)

    def test_songs(self) -> None:
        self.assertIsInstance(self.a.songs, list)
        self.assertTrue(len(self.a.songs) > 0)

    def test_str(self) -> None:
        self.assertEqual(str(self.a), "Stephane Bellanger")


class TestRainwaveListener(unittest.TestCase):
    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    listener = rw.channels[4].get_listener_by_id(3)

    def test_avatar(self) -> None:
        _avatar = "https://cdn.discordapp.com/avatars/137745037898416129/8ce1eddfcb8cf8ba0e5e22b920d3d8af.png?size=1024"
        self.assertEqual(self.listener.avatar, _avatar)

    def test_color(self) -> None:
        self.assertEqual(self.listener.color, "FF0000")

    def test_colour(self) -> None:
        self.assertEqual(self.listener.colour, "FF0000")

    def test_id(self) -> None:
        self.assertEqual(self.listener.id, 3)

    def test_losing_requests(self) -> None:
        self.assertEqual(self.listener.losing_requests, 0)

    def test_losing_votes(self) -> None:
        self.assertEqual(self.listener.losing_votes, 0)

    def test_mind_changes(self) -> None:
        self.assertEqual(self.listener.mind_changes, 0)

    def test_name(self) -> None:
        self.assertEqual(self.listener.name, "William")

    def test_rank(self) -> None:
        self.assertEqual(self.listener.rank, "Mister Three")

    def test_repr(self) -> None:
        self.assertEqual(repr(self.listener), "<RainwaveListener [William]>")

    def test_str(self) -> None:
        self.assertEqual(str(self.listener), "William")

    def test_total_ratings(self) -> None:
        self.assertEqual(self.listener.total_ratings, 0)

    def test_total_requests(self) -> None:
        self.assertEqual(self.listener.total_requests, 0)

    def test_total_votes(self) -> None:
        self.assertEqual(self.listener.total_votes, 0)

    def test_user_id(self) -> None:
        self.assertEqual(self.listener.user_id, 3)

    def test_winning_requests(self) -> None:
        self.assertEqual(self.listener.winning_requests, 0)

    def test_winning_votes(self) -> None:
        self.assertEqual(self.listener.winning_votes, 0)


@unittest.skip("These tests are unstable")
class TestRainwaveRequest(unittest.TestCase):
    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    rq = rw.channels[4].requests[0]

    def test_repr(self) -> None:
        self.assertTrue(repr(self.rq).startswith("<RainwaveRequest "))

    def test_requester(self) -> None:
        self.assertIsInstance(self.rq.requester.name, str)


class TestRainwaveCandidate(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
        cls.sched_next = cls.rw.channels[4].schedule_next[0]

    def setUp(self) -> None:
        if self.sched_next.type == "OneUp":
            self.skipTest("Next event is not an election")
        self.cand = self.sched_next.candidates[0]

    def test_repr(self) -> None:
        self.assertTrue(repr(self.cand).startswith("<RainwaveCandidate "))

    def test_entry_id(self) -> None:
        self.assertTrue(self.cand.entry_id > 0)

    def test_is_request(self) -> None:
        self.assertIsInstance(self.cand.is_request, bool)

    def test_requested_by(self) -> None:
        if self.cand.is_request:
            name = self.cand.requested_by.name
            self.assertIsInstance(name, str)
        else:
            self.assertTrue(self.cand.requested_by is None)

    def test_vote(self) -> None:
        current = self.rw.channels[4].schedule_current
        self.cand: rainwaveclient.RainwaveCandidate = (
            self.rw.channels[4].schedule_next[0].candidates[0]
        )
        now = datetime.datetime.now(datetime.timezone.utc)
        time_left: datetime.timedelta = current.end - now
        if int(time_left.total_seconds()) < 10:
            self.skipTest(f"{int(time_left.total_seconds())} left, skipping vote test")
        try:
            self.cand.vote()
        except Exception as e:
            if "You must be tuned in." in str(e):
                self.skipTest("Test user is not tuned in")


@unittest.skip("These tests are unstable")
class TestRainwaveUserRequest(unittest.TestCase):
    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)
    chan = rw.channels[4]
    album = chan.albums[sys.version_info.minor]
    song = album.songs[0]

    @classmethod
    def setUpClass(cls) -> None:
        in_urq = False
        for ur in cls.chan.user_requests:
            if ur.id == cls.song.id:
                in_urq = True
        if not in_urq:
            cls.song.request()

    @classmethod
    def tearDownClass(cls) -> None:
        for ur in cls.chan.user_requests:
            if ur.id == cls.song.id:
                ur.delete()

    def test_repr(self) -> None:
        urq = self.chan.user_requests
        self.assertTrue(repr(urq[0]).startswith("<RainwaveUserRequest"))

    def test_urq_len(self) -> None:
        urq = self.chan.user_requests
        self.assertTrue(len(urq) > 0)

    def test_urq_reorder(self) -> None:
        urq = self.chan.user_requests
        if len(urq) < 1:
            self.skipTest("Nothing in the user request queue")
        self.assertRaises(Exception, urq.reorder, [99])
        self.assertRaises(Exception, urq.reorder, [98, 99])
        indices = list(range(len(urq)))
        random.shuffle(indices)
        urq.reorder(indices)


class TestRainwaveSchedule(unittest.TestCase):
    rw = rainwaveclient.RainwaveClient(USER_ID, KEY)

    def test_id(self) -> None:
        event = self.rw.channels[4].schedule_current
        self.assertIsInstance(event.id, int)

    def test_repr(self) -> None:
        event = self.rw.channels[4].schedule_current
        self.assertTrue(repr(event).startswith("<Rainwave"))

    def test_start(self) -> None:
        event = self.rw.channels[4].schedule_current
        self.assertIsInstance(event.start, datetime.datetime)

    def test_start_actual_current(self) -> None:
        event = self.rw.channels[4].schedule_current
        self.assertIsInstance(event.start_actual, datetime.datetime)
        self.assertGreater(
            datetime.datetime.now(datetime.timezone.utc), event.start_actual
        )

    def test_start_actual_history(self) -> None:
        event = self.rw.channels[4].schedule_history[0]
        self.assertIsInstance(event.start_actual, datetime.datetime)

    def test_start_actual_next(self) -> None:
        event = self.rw.channels[4].schedule_next[0]
        self.assertIsNone(event.start_actual)


if __name__ == "__main__":
    notch.configure()
    ver = sys.version_info
    log.info(f"Testing on Python {ver.major}.{ver.minor}.{ver.micro}")
    unittest.main()
