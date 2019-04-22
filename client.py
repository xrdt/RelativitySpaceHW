#!/bin/bash/python3
import socket
import sys
import struct
import time
import pickle

def simple_control_loop(current_pos):
    if current_pos == 0: 
        return 0.
    else:
        return -.6 * current_pos


def json_encode(data): 
    return pickle.dumps({'move': data})


if __name__ == '__main__':
    # Don't have to close socket now
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: 
        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 10000)
        print('connecting to {} port {}'.format(*server_address))
        sock.connect(server_address)

        while True:
            # get data
            message = pickle.dumps({'sensor_data': 1})
            print('sending {!r}'.format(message))
            sock.sendall(message)

            # getting back the sensor data
            data = struct.unpack('!d', sock.recv(32))
            print('received {!r}'.format(data))

            # send back move command
            return_message = json_encode(simple_control_loop(data[0]))
            sock.sendall(return_message)
        
            # 1 Hz
            time.sleep(1. - time.time() % 1.) 
