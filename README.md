# G-Chat CLI

A command-line messaging application built in **Python**, using TCP sockets, multithreading, and a custom RSA-based encryption system.

## Features

* User registration and login with **Argon2 password hashing**
* Client-server messaging over **TCP sockets**
* Support for multiple concurrent clients
* Contact and conversation management
* Persistent message storage using **JSON**
* Custom **RSA-based message encryption**
* Background database worker using a **task queue**

## Technologies

**Python · TCP/IP · Sockets · Multithreading · RSA · Argon2 · JSON**

## Project Structure

```text
g-chat-cli/
├── client/
│   ├── client.py
│   ├── network.py
│   └── encryptor.py
├── server/
│   ├── server.py
│   └── records.py
└── README.md
```

## Running

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
python server/server.py
```

Then start a client in another terminal:

```bash
python client/client.py
```

Multiple clients can be run simultaneously to test communication.

