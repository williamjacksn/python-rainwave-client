from __future__ import unicode_literals

__setup_name__ = 'python-rainwave-client'
__version__ = '0.7.0'
__author__ = 'William Jackson'
__author_email__ = 'william@subtlecoolness.com'
__url__ = 'https://github.com/williamjacksn/python-rainwave-client'
__description__ = 'Python client library for Rainwave'
__keywords__ = 'rainwave client'

from .client import RainwaveClient
from .channel import RainwaveChannel
from .album import RainwaveAlbum
from .artist import RainwaveArtist
from .category import RainwaveCategory
from .schedule import RainwaveSchedule, RainwaveElection, RainwaveOneTimePlay
from .song import RainwaveSong, RainwaveCandidate
from .request import RainwaveRequest, RainwaveUserRequest
from .request import RainwaveUserRequestQueue
from .listener import RainwaveListener
