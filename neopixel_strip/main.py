
# Imports
import os
import time
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import neopixel
import board
import json

'''
nfoert's collection of scripts for setting up Raspberry Pi Pico W as smart home devices and sensors.

This is the NeoPixel LED strip. You should configure everything in the settings.toml file, and set the led data pin below.
The LED strip should be wired to GND, VBUS and GPIO of your choice.


Thanks to:
https://learn.adafruit.com/wifi-mailbox-notifier/code-the-wifi-mailbox-notifier
https://learn.adafruit.com/mqtt-in-circuitpython/overview
https://github.com/adafruit/Adafruit_CircuitPython_MiniMQTT/blob/main/examples/native_networking/minimqtt_adafruitio_native_networking.py

And various other Adafruit guides.

Sorry this one's sort of a mess, contributions welcome!

'''

pin = board.GP1


'''
----------
'''

switch = False
brightness = 0 # 0 / 255

pixels = neopixel.NeoPixel(pin, int(os.getenv("number_of_leds")))
r = 0
g = 0
b = 0
prev_r = 0
prev_g = 0
prev_b = 0

def set_rgb(transition=None): # TODO: Transition support
    global brightness
    global pixels
    global r
    global g
    global b

    new_r = int((r / 255) * brightness)
    new_g = int((g / 255) * brightness)
    new_b = int((b / 255) * brightness)

    print(new_r, new_g, new_b)

    pixels.fill((new_r, new_g, new_b))



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


# Functions for MQTT
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected to the broker
    print(f"Connected to broker! Listening for topic changes on topics")
    client.subscribe(os.getenv("mqtt_set_topic"))
    client.subscribe(os.getenv("mqtt_status_topic"))


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected from the broker
    print("Disconnected from the broker!")


def message(client, topic, message):
    global brightness
    global pixels
    global r
    global g
    global b
    global prev_r
    global prev_g
    global prev_b
    global mode
    # Ignore the global variable soup
    # This method is called when a topic the client is subscribed to has a new message
    print(f"New message on topic {topic}: {message}")
    message = json.loads(message)

    if topic == "nfoert/led1/set":
        try:
            brightness = message["brightness"]

        except:
            pass

        try:
            color = message["color"]
            prev_r = r
            prev_g = g
            prev_b = b
            r = color["r"]
            g = color["g"]
            b = color["b"]

        except:
            pass

        try:
            transition = message["transition"]

        except:
            transition = None

        try:
            state = message["state"]
            if state == "OFF":
                brightness = 0
                mode = False

            elif state == "ON":
                if mode == False:
                    brightness = 255
                    mode = True

                else:
                    pass

        except:
            pass
        
        # TODO: Update the broker with current status
        status = { 
            "state": state,
            "brightness":int(brightness),
            "color":{"r":r, "g":g, "b":b}
        }

        if transition:
            set_rgb(transition=transition)

        else:
            set_rgb(transition=3)



# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker = os.getenv("mqtt_ip"),
    port = os.getenv("mqtt_port"),
    username = os.getenv("mqtt_username"),
    password = os.getenv("mqtt_password"),
    socket_pool = pool,
    ssl_context = ssl_context,
)

# Setup the callback methods above
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

while True:
    # Poll the message queue
    mqtt_client.loop()

    # Send a new message
    time.sleep(int(os.getenv("refresh_rate")))


