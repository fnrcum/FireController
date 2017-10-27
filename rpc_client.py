from xmlrpc.client import ServerProxy
import subprocess
import os

if __name__ == "__main__":
    full_path = "2fab42c6-e260-473c-abfc-1725b7b3daeb"
    params = "TheIsland?listen?Port=7778?QueryPort=27014?MaxPlayers=2?bRawSockets?AllowCrateSpawnsOnTopOfStructures=True?RCONEnabled=True?RCONPort=32330?RCONServerGameLogBuffer=1 " \
             "-NoBattlEye -insecure -noantispeedhack -servergamelog -servergamelogincludetribelogs " \
             "-ServerRCONOutputTribeLogs -usecache -nosteamclient -game -server -log"
    s = ServerProxy('http://localhost:6160/rpc')
    s.start_server(full_path, params)