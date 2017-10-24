from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import argparse

__author__ = 'Nicu'


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

        def start_server(self, start_params):
            pass
            return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--localhost", help="connected to (default: %(default)s)",
                        default="https://localhost")
    parser.add_argument("-p", "--port", help="port the app_rpc server will listen on (default: %(default)s)",
                        default=6610, type=int)
    args = parser.parse_args()
    AppRPC(args.port)


if __name__ == '__main__':
    main()

