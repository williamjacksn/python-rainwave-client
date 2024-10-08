.. python-rainwave-client documentation master file, created by
   sphinx-quickstart on Thu Jun 20 15:42:32 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python Rainwave Client
======================

This is a Python client library for Rainwave_. The source is available at
https://github.com/williamjacksn/python-rainwave-client.

.. _Rainwave: https://rainwave.cc/

Installation
------------

Install using ``pip``::

    pip install python-rainwave-client


Getting Started
---------------

Begin by importing the library and instantiating a :class:`RainwaveClient`
object::

    >>> from rainwaveclient import RainwaveClient
    >>> rw = RainwaveClient()

Obtain your Rainwave User ID and API key from https://rainwave.cc/keys/ and set
them in the :class:`RainwaveClient` object::

    >>> rw.user_id = 5049
    >>> rw.key = 'abcde12345'
    >>> rw
    RainwaveClient(user_id=5049, key='abcde12345')

From the :class:`RainwaveClient` object you can get a list of channels
operating on the network::

    >>> rw.channels
    [<RainwaveChannel [Game]>, <RainwaveChannel [OCRemix]>, <RainwaveChannel [Covers]>, <RainwaveChannel [Chiptunes]>, <RainwaveChannel [All]>]
    >>> ocr = rw.channels[1]
    >>> ocr.key
    'ocremix'
    >>> ocr.url
    'https://rainwave.cc/ocremix/'
    >>> ocr.mp3_stream
    'http://ocrstream.rainwave.cc:8000/ocremix.mp3?5049:abcde12345'

See what is currently playing::

    >>> ocr.schedule_current.songs[0]
    <RainwaveCandidate [OCRemix // Final Fantasy VII: Voices of the Lifestream // Black Wing Metamorphosis // bLiNd, Fishy, Jillian Aversa, Sixto Sounds, Steffan Andrews, Suzumebachi, tefnek]>
    >>> # or ocr.schedule_current.song

Give the currently playing song a rating and mark it as a favourite::

    >>> ocr.schedule_current.songs[0].rating = 4.5
    >>> ocr.schedule_current.songs[0].fave = True

See what songs are in the current election::

    >>> ocr.schedule_next[0].candidates
    [<RainwaveCandidate [OCRemix // Castlevania II: Simon's Quest // Simon's Symphony // Jovette Rivera]>,
     <RainwaveCandidate [OCRemix // Sonic the Hedgehog: The Sound of Speed // Final Progression // Jewbei]>,
     <RainwaveCandidate [OCRemix // Friday the 13th // Panic at Camp Crystal // Ghetto Lee Lewis]>]

Vote for *Final Progression*::

    >>> ocr.schedule_next[0].candidates[1].vote()

API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   api
   changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
