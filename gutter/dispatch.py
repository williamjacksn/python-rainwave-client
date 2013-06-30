'''
Signalling framework for internal use.

This is loosely inspired by the Django signalling systems, although far more
minimalistic.

To use, either register a callable using your target signal's
:method:`Signal.connect(receiver)` or use :decorator:`receiver` as so:

    from gutter.channel import post_sync
    from gutter.dispatch import receiver

    @receiver(post_sync)
    def on_post_sync(signal, sender, **kwargs):
        ## do something here
'''

import threading

class Signal(object):
    '''
    A signal is triggered each time a particular event happens.
    '''
    
    def __init__(self):
        self.receivers = set()
        self.lock = threading.Lock()

    def connect(self, receiver):
        '''Adds a receiver to the signal.'''

        self.lock.acquire()
        try:
            self.receivers.add(receiver)
        finally:
            self.lock.release()

    def disconnect(self, receiver):
        '''Removes a receiver from the signal.'''

        self.lock.acquire()
        try:
            self.receivers.remove(receiver)
        finally:
            self.lock.release()

    def send(self, sender, **kwargs):
        '''Sends the signal to all connected receivers.'''

        for receiver in self.receivers:
            receiver(signal=self, sender=sender, **kwargs)

def receiver(signal, **kwargs):
    '''Decorator for registering a signal.'''

    def decorator(func):
        signal.connect(func, **kwargs)
    return decorator
