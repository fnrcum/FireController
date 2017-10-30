from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from subprocess import STDOUT, Popen, PIPE
import source_rcon as rcon
import datetime
from time import sleep
from orm import *

__author__ = 'Nicu'


class DateTimeFormatter(object):

    def __init__(self, now):
        self.now = now

    def return_datetime_object(self):
        now_frmt = self.now - datetime.timedelta(microseconds=self.now.microsecond)
        return now_frmt


class ServerRcon(object):
    def __init__(self, ip, port, password):
        self.ip = ip
        self.port = port
        self.password = password

    def run_command(self, ark_command):
        try:
            server = rcon.SourceRcon(self.ip, self.port, self.password, timeout=1)
            result = server.rcon(ark_command)
            return result
        except Exception as e:
            print('Unable to connect to RCON! \n {}'.format(e))


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

        def start_server(self, server_hash, config, params, rcon_port):
            s.execute(update(Server).where(Server.Id == server_hash).values(Status=201))
            s.commit()
            conn = ServerRcon(b"127.0.0.1", int(rcon_port), b"3hoxfxmjfS")
            time_start = DateTimeFormatter(datetime.datetime.now()).return_datetime_object()
            Popen(["start", server_hash+"\\ShooterGame\\Binaries\\Win64\\ShooterGameServer.exe", config + " " + params],
                  stdout=PIPE,
                  stderr=STDOUT,
                  shell=True,
                  bufsize=0)
            while conn.run_command(b"echo start") is None:
                sleep(1)
            time_end = DateTimeFormatter(datetime.datetime.now()).return_datetime_object() - time_start
            s.execute(update(Server).where(Server.Id == server_hash).values(LoadTime=int(time_end.total_seconds())))
            s.execute(update(Server).where(Server.Id == server_hash).values(Status=200))
            s.commit()
            return True

        def stop_server(self, server_hash, rcon_port):
            s.execute(update(Server).where(Server.Id == server_hash).values(Status=301))
            s.commit()
            conn = ServerRcon(b"127.0.0.1", int(rcon_port), b"3hoxfxmjfS")
            response = conn.run_command(b"DoExit")
            while conn.run_command(b"echo start") is not None:
                sleep(1)
            s.execute(update(Server).where(Server.Id == server_hash).values(Status=300))
            s.commit()
            return response


if __name__ == '__main__':
    AppRPC(6160)

