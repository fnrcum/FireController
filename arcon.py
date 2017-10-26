import valve.rcon

address = ("127.0.0.1", 27014)
password = "3hoxfxmjfS"
with valve.rcon.RCON(address, password) as rcon:
    response = rcon.execute("echo Hello, world!")
    print(response.text)