from socket import socket, AF_INET, SOCK_STREAM
from config import BUFFER_SIZE, SERVER_PORT, BINDIND_ADDR, MENU_STRING

from _thread import start_new_thread

from models.client import Client
from models.message import Message
from models.channel import Channel
from utils import Styles

clients = {}

channels = {}

SERVER_SOCKET: socket


def client_handler(client: Client):

    try:

        # Upon connection , the server will ask the client to enter a username and will keep asking until a valid username is entered
        while True:

            try:
                client.send_message(
                    f"{Styles.yellow.value}{Styles.bold.value}Enter your username (use /nick to change it) {Styles.end.value}")
                name: str = client.connection.recv(2048).decode()

                if not is_valid_username(name):
                    client.send_message(
                        f"{Styles.red.value}{Styles.bold.value}Username must start with @ and be alphanumeric with no spaces \n{Styles.end.value}"
                    )
                    continue

                if not is_username_available(name):
                    client.send_message(
                        f"{Styles.red.value}{Styles.bold.value}Username {name} is taken \n{Styles.end.value}"
                    )
                    continue

                client.name = name
                client.send_message(
                    f"{Styles.green.value}{Styles.bold.value}Username created successfully{Styles.end.value}")
                break
            except:
                client.should_disconnect = True
                break

        # Main loop for handling client commands
        while True:
            # check if the client should disconnect and close the connection
            if client.should_disconnect:
                client.connection.close()
                break

            # receive data from the client
            command = client.connection.recv(BUFFER_SIZE)
            if not command:
                del clients[client.address]
                for channel in channels.values():
                    if channel.owner == client:
                        del channels[channel.name]
                        break
                # remove channels
                break

            # decode the command and extract the message and parameters
            message = Message.decode(command)
            print(f"command from {client.name}: {command.decode()}")
            parameters = message.parameters
            print(f"command name: {message.command}")

            # Validate that request to server is a command
            if not message.command.startswith("/"):
                client.send_message(
                    f"{Styles.red.value}{Styles.bold.value}Join a channel to send messages{Styles.end.value}")
                continue

            # Handle the command
            match message.command[1:]:

                case "CHAN":
                
                    if not parameters[0]:
                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}Please input a channel name.{Styles.end.value}"
                        )
                        continue

                    channel_name = parameters[0]
                    if channel_name in channels.keys():

                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}Channel with name {channel_name} already exists{Styles.end.value}")
                        continue

                    if not is_valid_channel(channel_name):
                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}Channel name must start with # and be alphnumeric with no spaces{Styles.end.value}"
                        )
                        continue

                    for channel in channels.values():
                        if channel.owner == client:
                            client.send_message(
                                f"{Styles.red.value}{Styles.bold.value}You already own a channel{Styles.end.value}")
                        continue

                    if parameters[1] == "-s":
                        if not parameters[2]:
                            client.send_message(
                                f"{Styles.red.value}{Styles.bold.value}Secret Channels must have a passkey{Styles.end.value}"
                            )
                            continue

                    if not parameters[2]:
                        new_channel = Channel(
                            name=channel_name, owner=client)
                        channels[channel_name] = new_channel
                        client.send_message(
                            f"{Styles.green.value}{Styles.bold.value}{channel_name} has been created{Styles.end.value}")
                        refresh(new_channel)

                    else:
                        new_channel = Channel(
                            name=channel_name, owner=client, secret=True, password=parameters[2])
                        channels[channel_name] = new_channel
                        client.send_message(
                            f"{Styles.green.value}{Styles.bold.value}{channel_name} has been created{Styles.end.value}")

                case "HELP":
                    client.send_message(MENU_STRING)
                case "JOIN":
                    channel_name = parameters[0]

                    if not is_valid_channel(channel_name):
                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}Channel name must start with # and be alphnumeric with no spaces{Styles.end.value}"
                        )
                        continue

                    if not channels.get(channel_name):
                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}No channel found with that name{Styles.end.value}"
                        )
                        continue

                    if client == channels[channel_name].owner:
                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}You can't join your own channel{Styles.end.value}"
                        )
                        continue

                    if channels[channel_name].secret:
                        if not parameters[1]:
                            client.send_message(
                                f"{Styles.red.value}{Styles.bold.value}You must provide a passkey to join the secret channel{Styles.end.value}"
                            )
                            continue

                        if parameters[1] != channels[channel_name].password:
                            client.send_message(
                                f"{Styles.red.value}{Styles.bold.value}Incorrect passkey{Styles.end.value}"
                            )
                            continue

                    owner = channels[channel_name].owner

                    send_ip(client_from=client, client_to=owner, server=True)
                    send_ip(client_from=owner, client_to=client)
                    # multi-user chat
                    # try:
                    #     for member in channels[channel_name].members:
                    #         send_ip(client_from=client, client_to=member)
                    #         send_ip(client_from=member,client_to=client)
                    #     channels[channel_name].members.append(client)
                    # except:
                    #     #break if client doesn't support group chats
                    #     break
                    channels.pop(channel_name)
                    client.connection.close()
                    owner.should_disconnect = True
                    break

                case "QUIT":
                    client.send_message(
                        f"{Styles.green.value}{Styles.bold.value}Goodbye :({Styles.end.value}")
                    client.connection.close()
                    clients.pop(client.address)

                    for channel in channels.values():
                        if channel.owner.name == client.name:
                            channels.pop(channel.name)
                    break

                case "MODE":
                    if not parameters[0]:
                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}Mode needs at least 2 arguments{Styles.end.value}")
                        continue
                    channel_name = parameters[0]
                    if not is_valid_channel(channel_name):
                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}Channel name must start with # and be alphnumeric with no spaces{Styles.end.value}"
                        )
                        continue
                    owner = channels[channel_name].owner

                    if client == owner:
                        match parameters[1]:
                            case "-s":
                                if not parameters[2]:
                                    client.send_message(
                                        f"{Styles.red.value}{Styles.bold.value}Must specify a passkey to go secret mode{Styles.end.value}"
                                    )
                                    continue
                                channels[channel_name].secret = True
                                channels[channel_name].password = parameters[2]

                                client.send_message(
                                    f"{Styles.green.value}{Styles.bold.value}Mode has been changed successfully{Styles.end.value}"
                                )
                            case "-n":
                                channels[channel_name].secret = False
                                refresh(channels[channel_name])
                                client.send_message(
                                    f"{Styles.green.value}{Styles.bold.value}Mode has been changed successfully{Styles.end.value}"
                                )
                            case _:
                                client.send_message(
                                    f"{Styles.red.value}{Styles.bold.value}Mode must either be -s <passkey> (secret) or -n (public){Styles.end.value}"
                                )

                    else:
                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}Unauthorized action, you cannot change the mode of a channel you do not own{Styles.end.value}")

                case "LIST":

                    if len(channels) == 0 or all_channels_secret():
                        notification = f"{Styles.red.value}{Styles.bold.value}No channels available yet{Styles.end.value}"
                    else:
                        notification = f"""
{Styles.bold.value}{Styles.yellow.value}Here is the list of all channels:{Styles.end.value}\n"""
                        for channel in channels.values():
                            if not channel.secret:
                                notification += f"{Styles.bold.value}{Styles.voilet.value}{channel.name}{Styles.end.value} \n"

                    client.connection.send(notification.encode())

                case "NICK":
                    new_name = message.parameters[0]
                    if not is_valid_username(new_name):
                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}Username must start with @ and be alphnumeric with no spaces{Styles.end.value}"
                        )
                        continue

                    if not is_username_available(new_name):
                        client.send_message(
                            f"{Styles.red.value}{Styles.bold.value}Username {new_name} is taken{Styles.end.value}"
                        )

                    client.name = new_name
                    client.send_message(
                        f"{Styles.green.value}{Styles.bold.value}Username changed successfully{Styles.end.value}")
                case _:
                    client.send_message(
                        f"{Styles.red.value}{Styles.bold.value}Unsupported command{Styles.end.value}")

        # When the client disconnects, remove the client from the list of clients
        for channel in channels.values():
            if channel.owner == client:
                if channels.get(channel.name):
                    channels.pop(channel.name)
                    break

        if clients.get(client.address):
            clients.pop(client.address)
        client.connection.close()
    except:
        for channel in channels.values():
            if channel.owner == client:
                if channels.get(channel.name):
                    channels.pop(channel.name)
                    break

        if clients.get(client.address):
            clients.pop(client.address)
        client.connection.close()
        return



def all_channels_secret():
    for channel in channels.values():
        if not channel.secret:
            return False
    return True

def is_valid_channel(channel: str):
    return channel.startswith("#") and channel[1:].isalnum()


def is_valid_username(username: str):
    return username.startswith("@") and username[1:].isalnum()


def is_username_available(username: str):
    for c in clients.values():
        if c.name == username:
            return False
    return True


def is_registered(client: Client):
    return not client.name == ""


def message_all_clients(message):
    for client in clients.keys():
        client.send(message.encode())

# Change this to channel


def refresh(channel_to_send: Channel):
    """
    When a new channel is created, this function is called to notify all clients of the new channel
    """
    for _, client in clients.items():
        if client == channel_to_send.owner:
            continue
        client.send_message(
            f"{Styles.voilet.value}{Styles.bold.value}New channel {channel_to_send.name} available.{Styles.end.value}")


def send_ip(client_from: Client, client_to: Client, server=False):
    """
    When a client joins a channel, this function is called to send the IP address of the client to the owner of the channel
    """
    prefix: str
    if not server:
        prefix = "?"
    else:
        prefix = ">"
    client_to.send_message(
        f"{prefix}{client_from.name}@{client_from.address[0]}:{client_from.address[1]}"
    )


def start():
    """
    Entry point for the server
    Intializes the server socket and listens for incoming connections
    """
    with socket(AF_INET, SOCK_STREAM) as SERVER_SOCKET:
        SERVER_SOCKET.bind(BINDIND_ADDR)

        SERVER_SOCKET.listen()

        print(f'{Styles.green.value}{Styles.bold.value}Server is listening on port -> {SERVER_PORT} {Styles.end.value}')

        # Loop forever until client quits or connects to another client
        while True:

            # establish connection with client
            connection, client_address = SERVER_SOCKET.accept()

            c = Client(
                name="@guest", connection=connection, address=client_address)

            # add new client to the list of clients
            clients[client_address] = c
            client = clients[client_address]

            # start a new thread that handles communication with the client
            start_new_thread(client_handler, (client,))

        SERVER_SOCKET.close()


if __name__ == '__main__':
    # Starts the server
    start()
