#!/bin/bash/python3

'''
Author: Bianca Yang
Objective: Relativity Space Homework Assignment
Description: Write a simulator for a robotic welder that includes a closed loop controller, 
             some sensors, and a GUI for turning on an off sensors.
'''

import numpy as np
import datetime
import random
import time
import tkinter
from influxdb import InfluxDBClient
from multiprocessing import Process
from threading import Timer

# single y_pos sensor is on
sensor = True

# set up influxDB
client = InfluxDBClient(host='localhost', port=8086)
client.create_database('robot_sim')
client.switch_database('robot_sim')

global move
global current_pos
move = 0.
current_pos = 0

def generate_data(client):
    # incorporate control loop input
    global current_pos
    global move
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
    Timer(.1, generate_data, [client]).start()
    

def control_loop():
    global move, current_pos
    # very simple control mechanism.
    move = 0.

    # if current pos is negative, send a positive signal to partially correct
    if current_pos < 0:
        move = -.6 * current_pos
    # if current pos is positive, send a negative signal to partially correct
    elif current_pos > 0:
        move = -.6 * current_pos
    else:
        move = 0.

    Timer(1, control_loop).start()


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

if __name__ == '__main__':
    # Start the sensor gui
    sensor_window = tkinter.Tk()
    sensor_window.title('Sensor Control Panel')
    button = tkinter.Button(sensor_window, width=25)
    button['text'] = 'Stop y_pos sensor' 
    button['command'] = lambda: sensor_switch(button)
    button.pack()

    p1 = Process(target=generate_data, args=(client,))
    p1.run()
    p2 = Process(target=control_loop)
    p2.run()
    p3 = Process(target=gui_window, args=(sensor_window, button))
    p3.run()

