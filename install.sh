apt update
apt install -y python3.9 python3-pip
apt install -y git
git clone https://github.com/BobOwi/flask-mqtt.git 
cd flask-mqtt
pip3 install -r requirements.txt
python3 app.py
