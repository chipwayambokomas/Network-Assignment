# Chat Protocol Readme

## Overview

This project implements a flexible chat protocol with a hybrid client-server and peer-to-peer architecture. It allows users to create, join, and manage channels with various privacy settings while supporting both centralized and direct communication.

## Architecture

- **Client-Server**: Clients connect to a central signaling server via TCP for operations like discovering channels, authentication, and establishing connections with peers.
- **Peer-to-Peer**: After initial setup, clients can communicate directly with each other via UDP for more efficient and private communication.

## Features

- **Channel Management**: Create, join, and leave channels
- **Privacy Controls**: Set channel visibility with optional password protection
- **Notification System**: Receive alerts about new channels and activities
- **Enhanced CLI**: Color-coded interface for improved readability
- **Custom Commands**: Intuitive command structure for performing actions

## Protocol Design

### Message Format

Commands follow a specific structure prefixed with a forward slash (`/`):
```
/command <parameter1> <parameter2> [optional_parameters]
```

### Core Commands

- `/chan <channel_name> [mode] [passkey]` - Create a new channel
  - Example: `/chan #developers -s password1234` creates a secret channel
- `/join <channel_name> [passkey]` - Join an existing channel
- `/part` - Leave the current channel
- Other commands available for channel management and communication

### Response Structure

- Standard responses are sent as normal messages
- Special responses that require client processing are prefixed with specific symbols
  - Example: `>PeerUsername@176.192.0.1:5555` provides connection details for peer-to-peer communication

## Technical Implementation

### Client Components

- **TCP Connection Handler**: Establishes and maintains server connection
- **UDP Connection Handler**: Manages peer-to-peer communications
- **Message Processors**: Parse and handle different message types
- **Threading**: Separate threads for sending and receiving messages

### Server Components

- **Channel Registry**: Manages active channels and their properties
- **Authentication**: Verifies channel access credentials
- **Connection Broker**: Facilitates peer connections

## Getting Started

1. Ensure you have the required dependencies installed
2. Start the server application
3. Launch client applications
4. Create or join channels using the command interface

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/chan` | Create a new channel | `/chan #general` |
| `/chan` | Create a private channel | `/chan #private -s passkey123` |
| `/join` | Join an existing channel | `/join #general` |
| `/join` | Join a private channel | `/join #private passkey123` |
| `/part` | Leave current channel | `/part` |

## Example Usage

```
# Connect to the server
> TCP connection established

# Create a channel
> /chan #developers
> Channel #developers was created successfully

# Join a channel
> /join #developers
> Connected to peer: User1@192.168.1.10:5555

# Send messages
> Hello everyone!

# Leave a channel
> /part
> You have left the channel
```

## Connection Flow

1. Client connects to server via TCP
2. Client creates or joins a channel
3. Server provides peer connection details
4. Client establishes direct UDP connection with peers
5. Communication continues over UDP
6. When finished, client sends `/part` to leave channel

## Security Considerations

- Channel passwords are used for access control
- Peer-to-peer connections offer improved privacy for conversations
- Consider implementing additional encryption for sensitive communications

## Known Limitations

- No persistent message history
- Limited to text-based communication
- Manual peer connection management
