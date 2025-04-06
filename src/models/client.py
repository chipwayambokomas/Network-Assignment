"""
Client class to store client information
"""
class Client:

    def __init__(self, name, connection, address) -> None:

        self.name = name
        self.connection = connection
        self.address = address
        self.should_disconnect = False

    def send_message(self, message: str):
        self.connection.send(message.encode())
