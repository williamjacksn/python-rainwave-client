.. Gutter documentation master file, created by
   sphinx-quickstart on Thu Jun 20 15:42:32 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Gutter
======

Gutter is a Rainwave_ client framework for Python. The source is available at https://github.com/williamjacksn/gutter.

.. _Rainwave: http://rainwave.cc/

Getting Started
---------------

Begin by importing the library and instantiating a RainwaveClient object:

::

    >>> from gutter.client import RainwaveClient
    >>> rw = RainwaveClient()

Obtain your Rainwave User ID and API key from http://rainwave.cc/auth/ and set them in the RainwaveClient object:

::

    >>> rw.user_id = 5049
    >>> rw.key = u'abcde12345'
    >>> rw
    RainwaveClient(user_id=5049, key=u'abcde12345')

From the RainwaveClient object you can get a list of channels operating on the network:

::

    >>> rw.channels
    [RainwaveChannel(Rainwave), RainwaveChannel(OCR Radio), RainwaveChannel(Mixwave), RainwaveChannel(Bitwave), RainwaveChannel(Omniwave)]
    >>> ocr = rw.channels[1]
    >>> ocr.stream
    u'http://ocstream.rainwave.cc:8000/ocremix.mp3?5049:abcde12345'

API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

