import source_rcon as rcon


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


conn = ServerRcon("86.126.74.236", 32331, "3hoxfxmjfS")

# print(conn.run_command("echo Hello"))
print(conn.run_command("ServerChat hello"))