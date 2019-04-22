#!/bin/bash/python3
import socket
import sys
import time 
import datetime
import numpy as np
import struct
import pickle
import tkinter
from influxdb import InfluxDBClient
from multiprocessing import Process

def generate_data(client, current_pos, move):
    # incorporate control loop input
    current_pos = move + current_pos 

    current_time = datetime.datetime.now()
       
    if np.random.randint(0, 10) == 6: 
        # random error
        current_pos += np.random.normal()

    # send this data to influxDB 
    json_body = [{"measurement": "y_pos", "time": str(current_time), 
                  "fields": {"pos": float(current_pos)}}]
    client.write_points(json_body)

    if move != 0: 
        json_body = [{"measurement": "y_move_cmd", "time": str(current_time), 
                      "fields": {"cmd": float(move)}}]
        client.write_points(json_body)
 
    move = 0
    return current_pos, move


def sensor_switch(sensor, button):
    sensor = not sensor 

    if button['text'] == 'Stop y_pos sensor': 
        button['text'] = 'Start y_pos sensor'
    else: 
        button['text'] = 'Stop y_pos sensor'


def gui_window(window, button): 
    while True: 
        window.update()
        window.update_idletasks()



if __name__ == '__main__':
    # Start the sensor gui
    sensor = True
    sensor_window = tkinter.Tk()
    sensor_window.title('Sensor Control Panel')
    button = tkinter.Button(sensor_window, width=25)
    button['text'] = 'Stop y_pos sensor' 
    button['command'] = lambda: sensor_switch(sensor, button)
    button.pack()

    # set up influxDB
    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('robot_sim')
    client.switch_database('robot_sim')

    # Don't need to worry about closing the socket 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Bind the socket to the port
        server_address = ('localhost', 10000)
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)
        # Listen for incoming connections
        sock.listen(1)
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        print('connection from', client_address)

        current_pos = 0
        move = 0 

        while True:
            current_pos, move = generate_data(client, current_pos, move)
            data = connection.recv(32)
            data = pickle.loads(data)
            print('received {!r}'.format(data))
            if data.get('sensor_data'):
                print('sending data back to the client')
                if sensor: 
                    return_data = struct.pack('!d', current_pos)
                    connection.sendall(return_data)
                else: 
                    return_data = struct.pack('!d', 0.0)
                    connection.sendall(return_data)
            elif data.get('move'):
                move = data.get('move')
                print('cmd executed', client_address)
            else:
                pass
            sensor_window.update()
            sensor_window.update_idletasks()
