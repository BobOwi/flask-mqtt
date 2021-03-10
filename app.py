#!/usr/bin/env python
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'iotmqtt.htl-klu.at'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'htl-IoT'
app.config['MQTT_PASSWORD'] = 'iot..2015'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)
socketio = SocketIO(app, async_mode='threading')

#sensors = {
#   'temp00' : {'name':'tempLiving', 'value' : '21','location' : 'living'}
#}
sensors = {}


# The callback when connected
@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
    print('Connected!!')
    client.subscribe('4ahel/#')

# The callback message received
@mqtt.on_message()
def on_message(client, userdata, msg):
    global sensors
    topicTree=msg.topic.split("/")
    sensorName=topicTree[-1]
    if len(topicTree)>2:
        sensorLocation=topicTree[-2]
    else:
        sensorLocation='-'
        
    newSensor=False
        
    try:
        if sensorName not in sensors:
            newSensor=True
        sensors[sensorName]={'name':sensorName,'value':float(msg.payload.decode()),'location':sensorLocation}
        print ("mqtt rec: Sensor {}: {}".format(sensorName,msg.payload.decode()))
        if newSensor:
            socketio.emit('pageReload', {'data':'new'})
        else:
            socketio.emit('tempResponse', {'sensor':sensors[sensorName]['name'],'data': sensors[sensorName]['value'],'location': sensors[sensorName]['location']})
            #print(s)
    except:
        print("!! Error reading Sensor !!")
        pass
        
    for s in sensors:
        print("S-> {} \tname:{} \tvalue:{}".format(s,sensors[s]['name'],sensors[s]['value']))


@app.route("/")
def hello_world():
    return render_template("index.html", sensors=sensors)


@socketio.on('connect')
def test_connect():
    print ("Socket connected")

@socketio.on('my event')
def test_message(message):
    print ("Socket says:{}".format(message['data']))
    #emit('my response', {'data': message['data']})
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)