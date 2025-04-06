"""
This file defines the configuration for creating the socket interface for the client and server
"""

from utils import Styles

SERVER_PORT = 12336
BINDIND_ADDR = ("", SERVER_PORT)
BUFFER_SIZE = 2048

MENU_STRING = f"""

Here is the list of commands:

{Styles.bold.value}{Styles.yellow.value}/chan{Styles.end.value} {Styles.italic.value}<channel_name> <mode (optional)> <passkey (optional)>{Styles.end.value} 
    {Styles.italic.value}> creates a channel{Styles.end.value} 

{Styles.bold.value}/join{Styles.end.value} {Styles.italic.value}<channel_name> <passkey (optional)>{Styles.end.value} 
    {Styles.italic.value}> joins a channel{Styles.end.value} 

{Styles.bold.value}{Styles.green.value}/nick{Styles.end.value} {Styles.italic.value}<new_nickname>{Styles.end.value} 
    {Styles.italic.value}> changes the username of a user{Styles.end.value} 

{Styles.bold.value}{Styles.voilet.value}/list{Styles.end.value} 
    {Styles.italic.value}> lists public channels on the server{Styles.end.value} 

{Styles.bold.value}{Styles.beige.value}/mode{Styles.end.value} {Styles.italic.value}<channel> <mode>{Styles.end.value} 
    {Styles.italic.value}> allows clients to specify how they are seen by other{Styles.end.value} 
"""
