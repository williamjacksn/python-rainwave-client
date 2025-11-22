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

import threading
import typing

if typing.TYPE_CHECKING:
    from .channel import RainwaveChannel


class Signal:
    """A signal is triggered each time a particular event happens."""

    def __init__(self) -> None:
        self.receivers = set()
        self.lock = threading.Lock()

    def connect(self, _receiver: typing.Callable) -> None:
        """Add a receiver to the signal."""

        with self.lock:
            self.receivers.add(_receiver)

    def disconnect(self, _receiver: typing.Callable) -> None:
        """Remove a receiver from the signal."""

        with self.lock:
            self.receivers.remove(_receiver)

    def send(self, sender: "RainwaveChannel", **kwargs: typing.Any) -> None:  # noqa: ANN401
        """Send the signal to all connected receivers."""

        for _receiver in self.receivers:
            _receiver(signal=self, sender=sender, **kwargs)


def receiver(signal: "Signal", **kwargs: typing.Any) -> typing.Callable:  # noqa: ANN401
    """Decorator for registering a signal."""

    def decorator(func: typing.Callable) -> None:
        signal.connect(func, **kwargs)

    return decorator
