"""
Signalling framework for internal use.

This is loosely inspired by the Django signalling systems, although far more
minimalistic.

To use, either register a callable using your target signal's
:method:`Signal.connect(receiver)` or use :decorator:`receiver` like so:

    from rainwaveclient.channel import post_sync
    from rainwaveclient.dispatch import receiver

    @receiver(post_sync)
    def on_post_sync(signal, sender, **kwargs):
        ## do something here
"""

from __future__ import unicode_literals

import threading


class Signal:
    """A signal is triggered each time a particular event happens."""

    def __init__(self):
        self.receivers = set()
        self.lock = threading.Lock()

    def connect(self, _receiver):
        """Add a receiver to the signal."""

        with self.lock:
            self.receivers.add(_receiver)

    def disconnect(self, _receiver):
        """Remove a receiver from the signal."""

        with self.lock:
            self.receivers.remove(_receiver)

    def send(self, sender, **kwargs):
        """Send the signal to all connected receivers."""

        for _receiver in self.receivers:
            _receiver(signal=self, sender=sender, **kwargs)


def receiver(signal, **kwargs):
    """Decorator for registering a signal."""

    def decorator(func):
        signal.connect(func, **kwargs)
    return decorator
