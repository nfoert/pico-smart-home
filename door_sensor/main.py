
# Imports

import os
import time
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import board
import json
from digitalio import DigitalInOut, Direction, Pull
import alarm
import time

'''
nfoert's collection of scripts for setting up Raspberry Pi Pico W as smart home devices and sensors.

This is the door sensor. You should configure everything in the settings.toml file, and set the pin for the sensor below.
The sensor should be wired to your GPIO of choice and the 3v pin. (Pin 36)

The sensor wakes up when the pin is triggered (door is open) it waits until the door is closed before going back to sleep.


Thanks to:
https://learn.adafruit.com/deep-sleep-with-circuitpython/overview
https://learn.adafruit.com/wifi-mailbox-notifier/code-the-wifi-mailbox-notifier
https://github.com/bablokb/pico-sleepcurrent
https://learn.adafruit.com/mqtt-in-circuitpython/overview
https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT/blob/main/examples/native_networking/minimqtt_adafruitio_native_networking.py

And various other Adafruit guides.
Also big thanks to members of the Adafruit Discord for helping me sort out some deep sleep issues.

- studioStephe(she/they) - (@studiosteph)
- DJDevon3 - (@djdevon3)

Especially this comment after the fact by @studiosteph explaining exactly why my original code didn't work.
https://discord.com/channels/327254708534116352/537365702651150357/1128408036940197958
----------
'''

pin = board.GP1


'''
----------
'''


# Setup on-board LED and the door sensor
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

led.value = True

door_open = DigitalInOut(pin)
door_open.direction = Direction.INPUT
door_open.pull = Pull.DOWN

# Connect to the internet
print(f"Connecting to {os.getenv('WIFI_SSID')}")

while True:
    try:
        wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
        break
        
    except Exception as e:
        print(f"There was a problem connecting to WiFi! Trying again... {e}")
        time.sleep(0.5)
        continue

print(f"Connected to {os.getenv('WIFI_SSID')}!")


# MQTT Functions
def connected(client, userdata, flags, rc):
    # This function will be called when the client connects to the broker.
    print(f"Connected to broker! Listening for topic changes on topics")

    client.subscribe(os.getenv('mqtt_status_topic'))


def disconnected(client, userdata, rc):
    # This method is called when the client disconnects from the broker.
    print("Disconnected from the Broker")


def message(client, topic, message):
    # This method is called when a topic the client is subscribed to has a new message
    print(f"New message on topic {topic}: {message}")
    message = json.loads(message)

    if topic == os.getenv('mqtt_status_topic'):
        pass


# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker = os.getenv('mqtt_ip'),
    port = os.getenv('mqtt_port'),
    username = os.getenv('mqtt_username'),
    password = os.getenv('mqtt_password'),
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Setup the mqtt functions above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
print("Connecting to the broker...")
while True:
    try:
        mqtt_client.connect()
        break

    except Exception as e:
        print(f"There was a problem connecting to the broker! Trying again... '{e}'")
        time.sleep(0.5)
        continue

# Update the avaliability with Home Assistant
mqtt_client.publish(os.getenv('mqtt_avaliability_topic'), "online")

# Poll the message queue
mqtt_client.loop()

# The door must be opened to have triggered the pin alarm, so update the broker that the door did open
mqtt_client.publish(os.getenv('mqtt_status_topic'), '{"state":"ON"}')
print("Sent message to broker")

print("Waiting for door to close...")
while True:

    if door_open.value == False: # Door is open (We already updated the server so do nothing)
        pass

    elif door_open.value == True: # Door is closed (Update the server and shut off)
        print("Door is closed!")
        time.sleep(0.5)
        mqtt_client.publish(os.getenv('mqtt_status_topic'), '{"state":"OFF"}')
        print("Sent message to broker")
        time.sleep(0.5)
        door_open.deinit()
        pin_alarm = alarm.pin.PinAlarm(pin=pin, value=False, pull=False)
        break
        
    
    time.sleep(0.5)


led.value = False

print("----------")
print("Going to sleep...")

alarm.exit_and_deep_sleep_until_alarms(pin_alarm)