import argparse
import threading
from orm import *


def write_in_file(args, leftovers):
    if args.start and not args.stop:
        text = "start {0} {1}".format(args.path, [leftover for leftover in leftovers])
        cmd = [text.replace('[', "").replace(']', "").replace(",", "").replace("'", "")]
        # proc =
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
    write_in_file(args, leftovers)
