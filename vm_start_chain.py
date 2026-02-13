# Team Member: Adrian Thomas
# Github Repo: https://github.com/Pradakicks/ee250_lab4/tree/main

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import socket

USERNAME = "adrianth" 
PING_TOPIC = f"{USERNAME}/ping"
PONG_TOPIC = f"{USERNAME}/pong"
latest_pong = None

"""This function (or "callback") will be executed when this client receives
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe(PONG_TOPIC)
    print("Subscribed to", PONG_TOPIC)

"""Custom callback to handle subscribed messages."""
def on_message(client, userdata, msg):
    global latest_pong
    payload = msg.payload.decode().strip()
    try:
        latest_pong = int(payload)
        print("Received on", msg.topic, "payload =", latest_pong)
    except ValueError:
        print("Ignoring non-integer payload:", payload)


if __name__ == '__main__':
    #get IP address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    #create a client object
    client = mqtt.Client()

    #attach callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host="172.20.10.5", port=1883, keepalive=60)

    client.loop_start()
    time.sleep(1)

    # kick off chain with an initial ping value
    current_ping = 0
    client.publish(PING_TOPIC, str(current_ping))
    print("Publishing ping", current_ping, "to", PING_TOPIC)

    last_sent_ping = current_ping

    while True:
        if latest_pong is not None:
            current_ping = latest_pong + 1

            if current_ping != last_sent_ping:
                time.sleep(1)
                client.publish(PING_TOPIC, str(current_ping))
                print("Publishing ping", current_ping, "to", PING_TOPIC)
                last_sent_ping = current_ping

        time.sleep(0.1)

