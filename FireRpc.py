from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import io, time, sys
from subprocess import STDOUT, Popen

__author__ = 'Nicu'

servers = {}
output = {}
_params = " TheIsland?listen?Port=7778?QueryPort=27014?MaxPlayers=2?bRawSockets?AllowCrateSpawnsOnTopOfStructures=True?RCONEnabled=True?RCONPort=32330 " \
             "-NoBattlEye -insecure -noantispeedhack -servergamelog -servergamelogincludetribelogs " \
             "-ServerRCONOutputTribeLogs -usecache -nosteamclient -game -server -log"

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

        def start_server(self, server_hash, params):

            filename = '{}.log'.format(server_hash)
            with io.open(filename, 'w') as writer, io.open(filename, 'rb', 1) as reader:
                process = Popen(["start", server_hash+"\\ShooterGame\\Binaries\\Win64\\ShooterGameServer.exe", params],
                                stdout=writer,
                                stderr=STDOUT,
                                shell=True,
                                bufsize=0)
                # print("-----passed this------")
                while process.poll() is None:
                    sys.stdout.write(str(reader.read()))
                    # sys.stdout.flush()
                    time.sleep(0.5)
                    # Read the remaining
                sys.stdout.write(str(reader.read()))
                # sys.stdout.flush()

            # StartThread(id=server_hash, target=_start_server)
            return True

        def print_server_log(self, server_hash):
            print(output[server_hash])
            return output[server_hash]

        def stop_server(self, server_hash):
            StopThread(server_hash)


if __name__ == '__main__':
    AppRPC(6160)

