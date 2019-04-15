# RelativitySpaceHW

## Installation Instructions

This installation assumes you are installing on a Linux system. 

Install InfluxDB using these instructions: https://docs.influxdata.com/influxdb/v1.7/introduction/installation/

Install Grafana using these instructions: https://grafana.com/grafana/download 

Ensure you have python3 installed. 

Ensure you have the following python modules installed: 
tkinter
InfluxDBClient

Set up Grafana to read from InfluxDB, with database 'robot\_sim"


## Running Instructions

Clone the repository. 

Type 'python3 hw.py' into your terminal. 

You should see a window pop up with a button to start / stop the sensors. 
Click this button and you will see the results in Grafana. 


## Design Diagram

![design diagram](design.jpg)
