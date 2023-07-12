# Door Sensor
## Parts
- [Raspberry Pico W](https://www.adafruit.com/product/5526)
- [LED Strip](https://www.adafruit.com/product/2552)

## Assembly
**WARNING: Depending on the amount of LEDs you're driving, you may need to power the LED strip externally, as the Pico may not be able to provide enough power!**
1. Solder the LED strip to the board. (My strip only has 30 LEDs, so I'm OK with powering it directly.) Solder the **red wire** to the **VBUS** pin (Board pin 40). Solder the **black wire** to any **GND** pin. (I used board pin 3.) Solder the **white wire** to any GPIO on the board. (I chose GPIO 1, or board pin 2.) Ensure to update `main.py` with the pin you chose.
2. Plug the device into your computer [download](https://circuitpython.org/board/raspberry_pi_pico_w/) the latest version of Circuit Python. Drop the file into the drive that appeared in your File Explorer. Once It's finished copying, the board will restart and remount as `CIRCUITPY`. Drop the `lib`, `main.py` and `settings.toml` into the drive. Remove `code.py`. Don't forget to configure everything in `settings.toml` like your WiFi and MQTT settings.
3. You're finished! Ensure you've followed the Home Assistant setup instructions in `README.md`. Un-plug the device from your computer and plug it into a micro usb power source. Mount it anywhere you like. I put mine underneath the lip of a shelf that was on top of a table.

## TO-DO
- The devices auto-update main.py (If you have it enabled) from this repo when I make updates. It's sort of a pain to modify the code, especially if you have them tucked away somewhere.
- Setup transition support
- Home Assistant reports that the device's status is unknow. Figure out how the device can send it's current brightness and RGB back to Home Assistant.