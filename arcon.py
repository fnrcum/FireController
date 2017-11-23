import source_rcon as rcon


class ServerRcon(object):
    def __init__(self, ip: bytes, port: int, password: bytes):
        self.ip = ip
        self.port = port
        self.password = password

    def run_command(self, ark_command: bytes) -> bytes:
        try:
            server = rcon.SourceRcon(self.ip, self.port, self.password, timeout=1)
            result = server.rcon(ark_command)
            return result
        except Exception as e:
            print('Unable to connect to RCON! \n Reason: {}'.format(e))


conn = ServerRcon(b"82.76.101.145", 32331, b"3hoxfxmjfS")

# print(conn.run_command("echo Hello"))
print(conn.run_command(b"listplayers"))
