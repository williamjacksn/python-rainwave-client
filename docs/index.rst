.. python-rainwave-client documentation master file, created by
   sphinx-quickstart on Thu Jun 20 15:42:32 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Python Rainwave Client
======================

This is a Rainwave_ client library for Python. The source is available at
https://github.com/williamjacksn/python-rainwave-client.

.. _Rainwave: http://rainwave.cc/

Installation
------------

`Clone the repository`_ or `download a release`_ and unpack it. Install with
this command::

    python setup.py install

.. _Clone the repository: https://github.com/williamjacksn/python-rainwave-client
.. _download a release: https://github.com/williamjacksn/python-rainwave-client/releases

Getting Started
---------------

Begin by importing the library and instantiating a :class:`RainwaveClient`
object::

    >>> from rainwaveclient import RainwaveClient
    >>> rw = RainwaveClient()

Obtain your Rainwave User ID and API key from http://rainwave.cc/keys/ and set
them in the :class:`RainwaveClient` object::

    >>> rw.user_id = 5049
    >>> rw.key = 'abcde12345'
    >>> rw
    RainwaveClient(user_id=5049, key='abcde12345')

From the :class:`RainwaveClient` object you can get a list of channels
operating on the network::

    >>> rw.channels
    [<RainwaveChannel [Rainwave]>, <RainwaveChannel [OCR Radio]>, <RainwaveChannel [Mixwave]>, <RainwaveChannel [Bitwave]>, <RainwaveChannel [Omniwave]>]
    >>> ocr = rw.channels[1]
    >>> ocr.stream
    'http://ocstream.rainwave.cc:8000/ocremix.mp3?5049:abcde12345'

See what is currently playing::

    >>> ocr.schedule_current.songs[0]
    <RainwaveCandidate [OCR Radio // Crystalis // A Tale of the God Slayer // 4 Keys]>

Give the currently playing song a rating and mark it as a favourite::

    >>> ocr.schedule_current.songs[0].rating = 4.5
    >>> ocr.schedule_current.songs[0].favourite = True

See what songs are in the current election::

    >>> ocr.schedule_next[0].candidates
    [<RainwaveCandidate [OCR Radio // Dragon Quest III // Flight of Destiny // Russell Cox]>,
     <RainwaveCandidate [OCR Radio // Friday the 13th // Panic at Camp Crystal // Ghetto Lee Lewis]>,
     <RainwaveCandidate [OCR Radio // No More Heroes // The 51st // Homeslice]>]

Vote for *The 51st*::

    >>> ocr.schedule_next[0].candidates[2].vote()

API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

