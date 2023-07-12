# Raspberry Pi Pico Smart Home
**A collection of scripts for setting up Raspberry Pi Pico W as smart home devices and sensors.**

## How to use this repo
Each directory is for each kind of device. `main.py` is the main Python file that the microcontroller runs. `lib` contains any libraries that that specific device needs. `settings.toml` contains any configuration that each device needs. `mqtt.yaml` indicates the entity setup for each device in Home Assistant. `instructions.md` talks about the parts needed, what I used and how to solder everything together.

## Setting up Home Assistant and the Mosquito MQTT Broker
*This is a breif overview. Look up a tutorial if you'd like more details*
**Note: I used a Raspberry Pi for my server, so I'm explaining the setup for Raspberry Pi. If you're using a different platform, the steps should still apply after step 3**
1. [Download](https://www.raspberrypi.com/software/) the Raspberry Pi Imager. Install it on your system. Flash the latest version of Home Assistant to a Micro SD card using the Imager. Pop it in your Pi and plug it in. (Raspberry Pi 4 is reccomended. You *can* use Rpi 3B+ and other 3's but you may have poor performance.)
2. Connect your pi to Ethernet and go to `homeassistant.local` in your browser. (If this is not working, check the IP address in your router and go to `<ip_address>:8123`)
3. Wait for the initial setup to run.
4. Head to `Settings > Add-Ons > Add-On Store` and search or find the **Mosquito Broker**. Install it and enable `Start on Boot` and `Watch Dog`. Start the add-on. While you're here, also install the **File Editor** add-on. You'll need it later.
5. Head to `Settings > Devices & Services`. Check the discovered section for `MQTT`. Click **Configure**. Change the username and password and click **Next**. Just click **Next** again unless you want to customize anything on the next screen. 
6. Now update your `settings.toml` on your Pico with the username, password and ip address of your broker.
7. Open the File Editor add-on from the sidebar and click the folder icon. Locate `configuration.yaml`. Paste the contents of `mqtt.yaml` for the Pico device you're setting up at the bottom of `configuration.yaml`. Customize the `name`, `object_id`, and the `_topic` values. Ensure they match the `_topic` values you've setup in each device's `settings.toml`.
8. Repeat steps 6-7 for each Pico you're setting up.

## TO-DO
1. Smart Switch
2. Occupancy Sensor (With PIR sensor?)
3. Water Sensor (I have the parts, code coming soon!)