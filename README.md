# whatsgood

Simple communication application implemented using python socket communication.
It offers two features: chat and audio. 

Chat server uses network discovery to find clients on the network to connect to.
After the client is connected, messages are broadcasted using TCP.

Audio calling can handle multiple clients and works with an input stream and an output stream with audio being transported using UDP. 
