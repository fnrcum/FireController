from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import os
from subprocess import run

__author__ = 'Nicu'

servers = {}
output = {}


class StoppableThread(threading.Thread):
    """
    Implements a thread that can be stopped.
    """
    def __init__(self,  name, target):
        super(StoppableThread, self).__init__(name=name, target=target)
        self._status = 'running'

    def stop_me(self):
        if self._status == 'running':
            self._status = 'stopping'

    def stopped(self):
        self._status = 'stopped'

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


class AppRPC(object):
    def __init__(self, port):
        self.rpc_instance = SimpleXMLRPCServer(("localhost", port),
                                               requestHandler=AppRPC.RequestHandler,
                                               logRequests=True, allow_none=True)
        self.rpc_instance.register_introspection_functions()
        app_rpc = AppRPC.RPCFunctions()
        self.rpc_instance.register_instance(app_rpc)
        self.rpc_instance.serve_forever()

    # Restrict to a particular path.
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/rpc',)

    # Register an instance; all the methods of the instance are
    # published as XML-RPC methods (in this case, just 'div').
    class RPCFunctions:

        def __init__(self):
            self.__headers = {
                'Accept': 'application/rpc.ver.01'
            }

        def start_server(self, start_params, server_hash):

            def _start_server():
                run([start_params], shell=True, stdout=output[server_hash], stderr=output[server_hash])

            StartThread(id=server_hash, target=_start_server)
            return True

        def print_server_log(self, server_hash):
            print(output[server_hash])

if __name__ == '__main__':
    AppRPC(6160)

