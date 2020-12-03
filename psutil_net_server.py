import psutil
import datetime
import time
import json
import pprint
import pickle
import socket

out_file = str(datetime.datetime.now())
out_file = out_file.replace('-','').replace(':','').split('.')[0].replace(' ','_')
out_file = out_file + '.json'
print(out_file)

empty = []
with open(out_file, 'w') as fd:
    json.dump(empty, fd, sort_keys=True, indent=4)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 12346)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)



while True:
    # Listen for incoming connections
    sock.listen(1)

    # Wait for a connection
    print('waiting for a connection')
    conn, client_address = sock.accept()
    try:
        print('connection from', client_address)

        data = []
        while True:
            packet = conn.recv(1024)
            if not packet: 
                break
            print (packet)
            data.append(packet)
        data_arr = pickle.loads(b"".join(data))
        print (data_arr)
        
        with open(out_file, 'a') as fd:
            json.dump(data_arr, fd, sort_keys=True, indent=4)

    finally:
        # Clean up the connection
        print("Closing current connection")
        conn.close()


