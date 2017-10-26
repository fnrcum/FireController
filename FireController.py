import argparse
from xmlrpc.client import ServerProxy
# from orm import *


def start_stop_server(args, leftovers):
    if args.start and not args.stop:
        s = ServerProxy('http://localhost:6160/rpc')
        text = "{0}".format([leftover for leftover in leftovers])
        params = [text.replace('[', "").replace(']', "").replace(",", "").replace("'", "")]
        s.start_server(args.path, params)
    else:
        with open('controller.log', 'w') as f:
            f.write("Stopping {0}".format(args.path) + "\n200 - Server stopped ...")
        f.close()


if __name__ == "__main__":
    args = argparse.ArgumentParser(description='Process some arguments.')
    args.add_argument('-start', help='Start the server', action='store_true')
    args.add_argument('-stop', help='Stop the server', action='store_true')
    args.add_argument('-path', help='Insert server exe path', required=True)

    args, leftovers = args.parse_known_args()
    start_stop_server(args, leftovers)
