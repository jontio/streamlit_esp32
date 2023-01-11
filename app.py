import streamlit as st
import os
import numpy

import paho.mqtt.client as mqtt
import time
import ssl
import certifi

import random

image_count=0

def get_random_numpy():
    """Return a dummy frame."""
    return numpy.random.randint(0, 100, size=(32, 32))


st.title("ESP32 Camera over WIFI and MQTTS");

viewer = st.image(get_random_numpy(), width=480)
message = st.empty()

def on_connect(client, userdata, flags, rc):
    print("on_connect");
    global image_count
    image_count=0;
    if rc == 0:
        message.text("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
        client.subscribe(st.secrets["MQTT_PATH"])
    else:
        message.text("Connection failed")


def on_message(client, userdata, msg):
    global image_count
    image_count=image_count+1
    message.text("Image Received: "+str(image_count))
    viewer.image(msg.payload)
    
print("running main");

client = mqtt.Client("Python"+str(random.randint(0,1000000000)))
client.tls_set(cert_reqs=ssl.CERT_NONE) #no varification of cert
client.username_pw_set(st.secrets["MQTT_USER"],password=st.secrets["MQTT_PASSWORD"])
client.on_connect = on_connect
client.on_message = on_message
client.connect(st.secrets["MQTT_SERVER"], port=8883)
client.loop_forever()
