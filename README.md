# Socket Chatroom
This project was a socket-based computer program with server and clients that talk to each other, similar to a zoom chat room. These programs were written in Python to run on either a Unix or Windows operating system. I created three programs: server.py, client.py, constants.py. The server.py program accepts all incoming clients with the correct IP address and port number and handles all incoming messages and outgoing message information. The client.py creates the socket to connect to the server with the correct IP address and port number; also uses pyqt5 for its graphical user interface (GUI) for easy client use. The server.py and client.py utilize multithreading to handle each client effortlessly. The constants.py just keeps track of the port, IP address, buffer size, and encoding for messages. The design and programs are modular and use abstract data types for software re-use. The project was tested with different concrete test cases to test a large capacity of users and all of the chat room functionalities. All inputs for connecting to the server were tested to make sure they fit within their parameters. Both the Server and Client were tested to make sure if either one closes it won’t crash the other one. The server handles all incoming users and leaving users while also updating all other users connected to the server.

## Usage
server.py
```python
python3 server.py
```

client_ui.py
```python
python3 client_ui.py
```
