import paho.mqtt.client as mqtt
import time
from datetime import datetime
import socket

USERNAME = "adrianth"  
PING_TOPIC = f"{USERNAME}/ping"
PONG_TOPIC = f"{USERNAME}/pong"

latest_ping = None

"""This function (or "callback") will be executed when this client receives
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe(PING_TOPIC)
    print("Subscribed to", PING_TOPIC)

"""Custom callback to handle subscribed messages."""
def on_message(client, userdata, msg):
    global latest_ping
    payload = msg.payload.decode().strip()
    try:
        latest_ping = int(payload)
        print("Received on", msg.topic, "payload =", latest_ping)
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

    last_sent_pong = None

    while True:
        if latest_ping is not None:
            current_pong = latest_ping + 1

            # avoid re-sending the same value repeatedly
            if current_pong != last_sent_pong:
                time.sleep(1)
                client.publish(PONG_TOPIC, str(current_pong))
                print("Publishing pong", current_pong, "to", PONG_TOPIC)
                last_sent_pong = current_pong

        time.sleep(0.1)

