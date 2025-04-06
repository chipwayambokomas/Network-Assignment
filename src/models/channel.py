"""
Channel class to represent a channel owned by a client
"""

from models.client import Client


class Channel:

    def __init__(self, name,  owner: Client, secret=False, password="") -> None:
        self.name = name
        self.owner = owner
        self.secret = secret
        self.password = password
        #self.members = []
