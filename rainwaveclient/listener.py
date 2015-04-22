from __future__ import unicode_literals


class RainwaveListener(dict):
    """A :class:`RainwaveListener` object represents a radio listener."""

    #: The :class:`RainwaveChannel` the listener belongs to.
    channel = None

    def __init__(self, channel, raw_info):
        self.channel = channel
        super(RainwaveListener, self).__init__(raw_info)

    def __repr__(self):
        return '<RainwaveListener [{0}]>'.format(self)

    def __str__(self):
        return self.name

    @property
    def avatar(self):
        """The URL of the listener's avatar."""
        return 'http://rainwave.cc{0}'.format(self['avatar'])

    @property
    def color(self):
        """See :attr:`colour`."""
        return self.colour

    @property
    def colour(self):
        """A hexadecimal string representing the listener's colour on the
        forums."""
        return self['colour']

    @property
    def id(self):
        """The ID of the listener."""
        if 'id' in self:
            return self['id']
        return self['user_id']

    @property
    def losing_requests(self):
        """The number of requests made by the listener that lost their
        election."""
        return self['losing_requests']

    @property
    def losing_votes(self):
        """The number of votes the listeners has given to a song that lost an
        election."""
        return self['losing_votes']

    @property
    def mind_changes(self):
        """The total number of times the listener changed a song rating."""
        return self['mind_changes']

    @property
    def name(self):
        """The name of the listener."""
        return self['name']

    @property
    def rank(self):
        """A string representing the listener's title on the forums."""
        return self['rank']

    @property
    def total_ratings(self):
        """The total number of songs the listener has rated."""
        return self['total_ratings']

    @property
    def total_requests(self):
        """The total number of requests the listener has made."""
        return self['total_requests']

    @property
    def total_votes(self):
        """The number of votes the listener has cast in the last two weeks."""
        return self['total_votes']

    @property
    def user_id(self):
        """See :attr:`id`."""
        return self.id

    @property
    def winning_requests(self):
        """The number of requests made by the listener that won their
        election."""
        return self['winning_requests']

    @property
    def winning_votes(self):
        """The number of votes the listener has given to a song that won an
        election."""
        return self['winning_votes']
