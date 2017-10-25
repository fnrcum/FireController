from xmlrpc.client import ServerProxy
import subprocess
import os

if __name__ == "__main__":
    # print(os.environ['COMSPEC'])
    # full_path = "2fab42c6-e260-473c-abfc-1725b7b3daeb\\ShooterGame\\Binaries\\Win64\\ShooterGameServer.exe"
    full_path = "2fab42c6-e260-473c-abfc-1725b7b3daeb/ShooterGame/Binaries/Win64/ShooterGameServer.sh"
    s = ServerProxy('http://localhost:6160/rpc')
    s.start_server("{0}".format(full_path), "2fab42c6-e260-473c-abfc-1725b7b3daeb")
    # print(s.print_server_log("2fab42c6-e260-473c-abfc-1725b7b3daeb"))
    # subprocess.run("start {} TheIsland".format(full_path), shell=True)