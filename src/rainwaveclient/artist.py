import typing

if typing.TYPE_CHECKING:
    from . import RainwaveChannel, RainwaveSong


class RainwaveArtist(dict):
    """A :class:`RainwaveArtist` object represents one artist.

    .. note::

        You should not instantiate an object of this class directly, but rather
        obtain one from :attr:`RainwaveChannel.artists` or
        :attr:`RainwaveSong.artists`.
    """

    def __init__(self, channel: "RainwaveChannel", raw_info: dict) -> None:
        self._channel = channel
        super().__init__(raw_info)

    def __repr__(self) -> str:
        return f"<RainwaveArtist [{self}]>"

    def __str__(self) -> str:
        return self.name

    @property
    def channel(self) -> "RainwaveChannel":
        """The :class:`RainwaveChannel` object associated with the artist."""
        return self._channel

    @property
    def id(self) -> int:
        """The ID of the artist."""
        return self["id"]

    @property
    def name(self) -> str:
        """The name of the artist."""
        return self["name"]

    @property
    def song_count(self) -> int:
        """The number of songs attributed to the artist."""
        return len(self.songs)

    @property
    def songs(self) -> list["RainwaveSong"]:
        """A list of :class:`RainwaveSong` objects attributed to the artist."""
        if "song_objects" not in self:
            self["song_objects"] = []
            for albums in self["all_songs"].values():
                for album_songs in albums.values():
                    for raw_song in album_songs:
                        song = self.channel.get_song_by_id(raw_song["id"])
                        self["song_objects"].append(song)
        return self["song_objects"]
