"""
Message class models the message that is sent between the server and the client
"""
class Message:
    
    def __init__(self, command, paramaters) -> None:
        self.command = command
        self.parameters = paramaters

    def encode(self) -> bytes:
        result_str = self.command + " "
        for i in self.parameters:
            result_str += i + " "

        return result_str.encode()

    @staticmethod
    def decode(data: bytes):
        """
        Decodes a message request and returns a Message object with the command and parameters
        """
        data_str = data.decode()
        data_array = data_str.split(" ")
        command: str = data_array[0].upper()

        parameters = []

        result = Message(command=command, paramaters=parameters)

        print(data_str)
        match command[1:]:

            case "CHAN":
                """
                CHAN <CHANNEL_NAME> <MODE (OPTIONAL)> <PASSKEY (OPTIONAL)>
                
                Default mode is -n : normal mode
                If mode -s : secret, passkey must be specified
                """
                if len(data_array) == 1:
                    parameters.append(None)
                    parameters.append(None)
                    parameters.append(None)
                else:
                    parameters.append(data_array[1])
                    if len(data_array) > 2:
                        parameters.append(data_array[2])
                        if len(data_array)>3:
                            parameters.append(data_array[3])
                        else:
                            parameters.append(None)
                    else:
                        parameters.append(None)
                        parameters.append(None)
            case "JOIN":
                """
                JOIN <CHANNEL> <KEY (optional)>
                Used by client to join a channel listed on the server
                """
                parameters.append(data_array[1])
                if len(data_array) > 2:
                    parameters.append(data_array[2])
                else:
                    parameters.append(None)

            case "QUIT":
                """
                JOIN <CHANNEL> <KEY (optional)>
                A client session is ended with a quit message. The server must close the connection to client which sends a QUIT message
                """
            case "NICK":
                """
                NICK <NEW_NICKNAME>
                Used to change previous nickone
                """
                if len(data_array) > 1:
                    parameters.append(data_array[1])
            case "HELP":
                """
                HELP
                Displays the commands menu
                """
            case "LIST":
                """
                LIST
                Used to list channels on the server
                """
            case "MODE":
                """
                MODE <CHANNEL> <MODE_TYPE> <KEY (OPTIONAL)>
                -s: secret mode
                -n: normal mode
                
                If entering secret mode, user must input a password that other users will use to gain access

                Allows clients to specify how they are seen by others
                """
                if len(data_array) > 2:
                    parameters.append(data_array[1])
                    parameters.append(data_array[2])
                    if len(data_array) > 3:
                        parameters.append(data_array[3])
                    else:
                        parameters.append(None)
                else:
                    parameters.append(None)
                    parameters.append(None)
                    parameters.append(None)

        return Message(command=command, paramaters=parameters)