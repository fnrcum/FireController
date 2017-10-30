import argparse
from xmlrpc.client import ServerProxy


def start_stop_server(args, leftovers):
    if args.start and not args.stop:
        s = ServerProxy('http://localhost:6160/rpc')
        s.start_server(args.path, args.config, args.params, int(args.rcon))
    else:
        s = ServerProxy('http://localhost:6160/rpc')
        s.stop_server(args.path, int(args.rcon))


if __name__ == "__main__":
    args = argparse.ArgumentParser(description='Process some arguments.')
    args.add_argument('-start', help='Start the server', action='store_true')
    args.add_argument('-stop', help='Stop the server', action='store_true')
    args.add_argument('-path', help='Insert server exe path', required=True)
    args.add_argument('-rcon', help='rcon port for the commands', required=True)
    args.add_argument('-config', help='initial part of the config for the server', required=True)
    args.add_argument('-params', help='initial part of the config for the server', required=True)

    args, leftovers = args.parse_known_args()
    print(args.params)
    start_stop_server(args, leftovers)
