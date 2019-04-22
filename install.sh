sudo apt-get update
# Install Grafana
wget https://dl.grafana.com/oss/release/grafana_6.1.4_amd64.deb
sudo dpkg -i grafana_6.1.4_amd64.deb
# Check checksum
sha256sum grafana_6.1.4_amd64.deb | awk '$1=="1ce4d2cfaaee4f152a56788d7c3edf09dca177a0393f7cb5eaf5963ef0304335"{print"grafana good to go"}'

# Start Grafana service
systemctl daemon-reload
systemctl start grafana-server

# Install InfluxDB
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.6_amd64.deb
sudo dpkg -i influxdb_1.7.6_amd64.deb
# Check checksum
sha256sum influxdb_1.7.6_amd64.deb | awk '$1=="f03dde115104de8d50f724542a3514409b7c8d3b146d18ccd21b045187b0704c"{print"influxdb good to go"}'

# Start InfluxDB service
sudo apt-get -y update && sudo apt-get -y install influxdb
sudo service influxdb start

# Install python
sudo apt -y install python3.6

# Store things in virtualenv
sudo apt-get -y install build-essential libssl-dev libffi-dev python-dev
sudo apt -y install python3-pip
sudo apt -y install python3-venv
mkdir ~/python-virtual-environments && cd ~/python-virtual-environments
python3 -m venv env
source env/bin/activate

# install modules 
pip3 install influxdb
sudo apt install python3-tk
