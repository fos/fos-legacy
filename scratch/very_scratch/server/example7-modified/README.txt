Architecture

The main thread listens for and accepts new socket connections. The TCP/IP connection is first wrapped by a WebSocket and then a Connection object, which is then handed off to the requested Application to be verified. 

WebSocket is responsible for reading from the underlying socket and parsing the data into commands based on the web socket protocol. Connection is a higher-level, thread-safe object used to abstract reading and writing from the web socket connection so it can be treated in a producer-consumer fashion.

Once verified, the Connection is then handed off to be shared by both the Application as well as the ConnectionManager. The ConnectionManager runs in its own thread and is responsible for filling each Connection's read queue and emptying its write queue so that data can flow between the client and the Application.

Specific Applications are requested based on the web socket URL used. For example, tictactoe.html requests ws://localhost:5678/tictactoe, which tries to join the Application instance running at /tictactoe

Instances of Applications are specified in the config.txt file. Each instance is run in its own thread.

Applications understand a pipe-delimited command format: "command|param1|param2"

Playing the Tic-Tac-Toe demo
1)Run webSocketServer.py
2)Using a browser that supports web sockets, such as Chrome, open tictactoe.html in two tabs.
3)In one tab click "Start"
4)Copy the game GUID that is shown in the logging panel on the right. Paste that into the "join" text field on the other tab and click "Join"
5)Enjoy some intense Tic-Tac-Toe action!

