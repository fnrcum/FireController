from xmlrpc.client import ServerProxy

s = ServerProxy('http://localhost:6160/rpc')
s.start_server("start 2fab42c6-e260-473c-abfc-1725b7b3daeb\ShooterGame\Binaries\Win64\ShooterGameServer.exe TheIsland",
               "2fab42c6-e260-473c-abfc-1725b7b3daeb")