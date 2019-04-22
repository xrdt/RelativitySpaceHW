#!/bin/bash/python3

'''
Author: Bianca Yang
Objective: Relativity Space Homework Assignment
Description: Write a simulator for a robotic welder that includes a closed loop controller, 
             some sensors, and a GUI for turning on an off sensors.
'''

import sockets
import numpy as np
import datetime
import random
import time
import tkinter
from influxdb import InfluxDBClient
from multiprocessing import Process
from threading import Timer

move = 0.
current_pos = 0

# single y_pos sensor is on
sensor = True


def generate_data(client):
    # incorporate control loop input
    current_pos = move + current_pos 

    current_time = datetime.datetime.now()
       
    if np.random.randint(0, 10) == 6: 
        # random error
        current_pos += np.random.normal()

    # send this data to influxDB 
    json_body = [{"measurement": "y_pos", "time": str(current_time), 
                  "fields": {"pos": current_pos}}]
    client.write_points(json_body)

    if move != 0: 
        json_body = [{"measurement": "y_move_cmd", "time": str(current_time), 
                      "fields": {"cmd": move}}]
        client.write_points(json_body)

    move = 0
    # 2 Hz
    Timer(.5, generate_data, [client]).start()
    

def sensor_switch(button):
    global sensor
    sensor = not sensor 

    if button['text'] == 'Stop y_pos sensor': 
        button['text'] = 'Start y_pos sensor'
    else: 
        button['text'] = 'Stop y_pos sensor'

def gui_window(window, button): 
    while True: 
        window.update()
        window.update_idletasks()


HOST = '127.0.0.1'
PORT = 65432

if __name__ == '__main__':
    # Start the sensor gui
    sensor_window = tkinter.Tk()
    sensor_window.title('Sensor Control Panel')
    button = tkinter.Button(sensor_window, width=25)
    button['text'] = 'Stop y_pos sensor' 
    button['command'] = lambda: sensor_switch(button)
    button.pack()

    # set up influxDB
    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('robot_sim')
    client.switch_database('robot_sim')

    # open up the server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

    p1 = Process(target=generate_data, args=(client,))
    p1.run()
    p3 = Process(target=gui_window, args=(sensor_window, button))
    p3.run()
