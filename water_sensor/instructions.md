# Water Sensor

**The code is setup for a sensor that is usually dry and sometimes wet. Changes need made to `main.py` if it's the other way around.**
## Parts
- [Raspberry Pico W](https://www.adafruit.com/product/5526)
- [Battery Holder](https://www.adafruit.com/product/4193)
- [Water Sensor](https://www.adafruit.com/product/4965)

## Assembly
1. Solder the battery holder to the board. **Red wire** to **VBUS** (Board pin 40). **Black wire** to any **GND** (I chose board pin 38)
2. Solder the sensor to the board solder the **White wire** to your choice of GPIO. (I chose GP1, board pin 2) Ensure you update the pin in `main.py`, then solder the **Red wire** to the **VSYS** pin (Board pin 39), finally solder the **Black wire** to your choice of **GND**.
3. Plug the device into your computer and [download](https://circuitpython.org/board/raspberry_pi_pico_w/) the latest version of Circuit Python. Drop the file into the drive that appeared in your File Explorer. Once It's finished copying, the board will restart and remount as `CIRCUITPY`. Drop the `lib`, `main.py` and `settings.toml` into the drive. Remove `code.py`. Don't forget to configure everything in `settings.toml` like your WiFi and MQTT settings.
4. Next, setup your SMS message integration if you desire it. Use a file editor add on for Home Assistant and navigate to `configuration.yaml` paste the `notify:` section in `notify.yaml` into the bottom of your Home Assistant's `configuration.yaml` file. Next, change some fields like your `server:` if you're not using Gmail. Change `sender:` and `username:` to your email address. If you're using Gmail, configure an App Password by going to [this page](https://myaccount.google.com/), type "App Passwords" into the search box and sign in. Click the "Select App" drop down and change it to "Other *(Custom Name)*". Give it a name like "homeassistant-smpt" and paste the code that is generated into the `password:` field. Next, change the `recipient:` field by first typing your phone number and follow that by `@domain` where `domain` is the domain for the SMS gateway for your numbers's carrier. Some common US ones are listed below, for more, check [here](https://en.wikipedia.org/wiki/SMS_gateway#Email_clients).
    - AT&T - **txt.att.net**
    - T-Mobile - **tmomail.net**
    - Verizon Wireless - **vtext.com**
<br>You can also use MMS if you desire, however you probably won't be sending images from your automation.
5. Next, create a [basic automation](./automation.png) to send the SMS. I've also added a action to send a notification to my Home Assistant mobile app.
6. You're finished! Ensure you've followed the Home Assistant setup instructions in `README.md`. Un-plug the device from your computer, put two AA batteries in the holder and press the switch on the battery holder. You'll have to experiment with the correct placing for the sensor. If you're placing it in an area that is often wet, try to use longer wires (But not too long, you may experience interference!) and place the actual Pico W and the batteries somewhere that they won't get wet.

## TO-DO
- The devices auto-update `main.py` (If you have it enabled) from this repo when I make updates. It's sort of a pain to modify the code, especially if you have them tucked away somewhere.
- Make a STL for 3D printing an enclosure
- Support for inverted usage (Wet more than dry)