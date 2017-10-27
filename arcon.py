import source_rcon as rcon


class ServerRcon(object):
    def __init__(self, ip, port, password, ark_command):
        self.ip = ip
        self.port = port
        self.password = password
        self.ark_command = ark_command

    def run_command(self):
        try:
            server = rcon.SourceRcon(self.ip, self.port, self.password, timeout=10)
            result = server.rcon(self.ark_command)
            return result
        except Exception as e:
            print('Unable to connect to RCON! \n {}'.format(e))


conn = ServerRcon("192.168.1.101", 27015, "3hoxfxmjfS", "echo Hello, world")

conn.run_command()