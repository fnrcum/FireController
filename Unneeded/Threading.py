import threading

servers = {}


class StoppableThread(threading.Thread):
    """
    Implements a thread that can be stopped.
    """
    def __init__(self,  name, target):
        super(StoppableThread, self).__init__(name=name, target=target)
        self._status = 'running'
        self._stop_event = threading.Event()

    def stop_me(self):
        if self._status == 'running':
            self._status = 'stopping'
        self._stop_event.set()

    def stopped(self):
        self._status = 'stopped'
        self._stop_event.is_set()

    def is_running(self):
        return self._status == 'running'

    def is_stopping(self):
        return self._status == 'stopping'

    def is_stopped(self):
        return self._status == 'stopped'


def StartThread(id, target):
    """
    Starts a thread and adds an entry to the global dThreads dictionary.
    """
    servers[id] = StoppableThread(name=id, target=target)
    servers[id].start()


def StopThread(id):
    """
    Stops a thread and removes its entry from the global dThreads dictionary.
    """
    thread = servers[id]
    if thread.is_running():
        thread.stop_me()
        thread.join()
        del servers[id]
