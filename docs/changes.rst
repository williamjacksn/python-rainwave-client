.. _changes:

=======
Changes
=======

2024.3
======

Released 2024-08-19.

* This release fixes severe bugs related to aware ``datetime`` objects in Python 3.8, 3.9, and 3.10.
* Type hints were added throughout the library.
* Some documentation strings were updated to be more clear.
* The ``RainwaveCandidate`` object has a new property ``election`` to access the ``RainwaveElection``
  that it belongs to.

2024.2
======

Released 2024.08.19.

The following ``datetime`` objects now have time zone info attached:

* ``RainwaveAlbum.added_on``
* ``RainwaveAlbum.cool_lowest``
* ``RainwaveAlbum.played_last``
* ``RainwaveSchedule.start``

The documentation for ``RainwaveSchedule.start`` has been clarified: this is an *estimated* start time for the event.
Even after an event occurs, this property will not give an accurate start time for the event.

``RainwaveSchedule`` gained the following new properties:

* ``start_actual`` (a ``datetime``) gives the real start time for a current or past event. For events that have not
  started yet, this property is ``None``.
* ``end`` (a ``datetime``) gives the end time for an event. For events that have not started, the end time is estimated.
  For events that have already started, the end time is exact.
* ``length`` (an ``int``) gives the duration in seconds for an event. For future elections, this property is the average
  of the durations of all songs in the election. ``RainwaveSchedule`` objects now also support ``len()``.

``RainwaveClient.call()`` has been updated to make API requests using ``POST`` instead of ``GET``. This should resolve
many bugs and "Missing ... data in API response" errors. If you use ``call()`` directly you can override the request
method with the new ``method=`` argument.

2024.1
======

Released 2024-02-09.

* Drop support for Python versions older than 3.9.
* Fixed a bug where the following properties of ``RainwaveAlbum``
  would not resolve correctly:

  * ``art``
  * ``added_on``
  * ``categories``
  * ``played_last``
  * ``rating_count``
  * ``rating_histogram``
  * ``rating_rank``
  * ``request_count``
  * ``request_rank``
  * ``songs``
  * ``vote_count``

* Type hints were added for several classes.

0.10.0
======

Released 2022-04-08.

* Drop support for Python versions older than 3.7.
* Emit log messages when certain information is expected in the API response but not found.

0.9.0
=====

Released 2022-01-27.

``RainwaveAlbum`` gained a new property:

* ``url`` (a ``str``) gives the URL of the album info page on https://rainwave.cc

``RainwaveChannel`` gained some new properties:

* ``key`` (a ``str``) gives a short string that identifies the channel.
* ``url`` (a ``str``) gives the URL of the web interface for the channel.

``RainwaveElection`` gained a new property:

* ``song`` (a ``RainwaveCandidate``) gives the first candidate in the list of candidates. If the ``RainwaveElection``
  has already ended, this is the song that won the election.

0.8.0
=====

Released 2022-01-26.

``RainwaveOneTimePlay`` gained a new property:

* ``songs`` gives a list containing the ``RainwaveSong`` for this event. Now you can use ``songs`` on any subclass of
  ``RainwaveSchedule`` to get the songs for an event.

0.7.0
=====

Released 2022-01-19.

The library is better at tracking when cached schedule information is stale and needs to be reloaded.

0.6.3
=====

Released 2020-07-09.

Switch to a new theme for the documentation.

0.6.2
=====

Released 2019-09-23.

Fix a link in the README.

0.6.1
=====

Released 2019-09-23.

Fix the package description for PyPI.

0.6.0
=====

Released 2019-09-23.

Drop support for Python 2.6, 3.2, 3.3, and 3.4. This version is supported on Python 2.7, 3.5, 3.6, and 3.7

* Base URLs now use ``https`` instead of ``http``.
* ``RainwaveAlbum.fave`` now returns ``False`` instead of ``None`` if the album is not a favourite.
* ``RainwaveUserRequestQueue`` gained a new method ``clear()`` to clear the user's request queue.

0.5
===

Released 2019-01-03.

The library now adds a randomly-generated user agent to each request.

0.4
===

Released 2015-04-22.

This version is supported on Python 2.6, 2.7, 3.2, 3.3, and 3.4.

0.3.1
=====

Released 2015-04-21.

The library has been renamed from *Gutter* to *Python Rainwave Client*.
