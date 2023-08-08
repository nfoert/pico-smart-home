# Door Sensor
**This could also be a window sensor, or anything that opens and closes.**

**The code is setup for a door that is usually closed and sometimes open. Changes need made if It's the other way around**
## Parts
- [Raspberry Pico W](https://www.adafruit.com/product/5526)
- [Battery Holder](https://www.adafruit.com/product/4193)
- [Door Sensor](https://www.adafruit.com/product/375)

## Assembly
1. Solder the battery holder to the board. **Red wire** to **VSYS** (Board pin 39). **Black wire** to any **GND** (I chose board pin 38)
2. Solder the sensor to the board. **One wire** to your choice of GPIO. (I chose GP1, board pin 2) Ensure you update the pin in `main.py`. Solder the **other wire** to the **3V3** pin (Board pin 36)
3. Plug the device into your computer [download](https://circuitpython.org/board/raspberry_pi_pico_w/) the latest version of Circuit Python. Drop the file into the drive that appeared in your File Explorer. Once It's finished copying, the board will restart and remount as `CIRCUITPY`. Drop the `lib`, `main.py` and `settings.toml` into the drive. Remove `code.py`. Don't forget to configure everything in `settings.toml` like your WiFi and MQTT settings.
4. You're finished! Ensure you've followed the Home Assistant setup instructions in `README.md`. Un-plug the device from your computer, put two AA batteries in the holder and press the switch on the battery holder. You'll have to experiment with the correct spacing for the sensor when you attach it to a door.

## TO-DO
- The devices auto-update main.py (If you have it enabled) from this repo when I make updates. It's sort of a pain to modify the code, especially if you have them tucked away somewhere.
- Make a STL for 3D printing an enclosure
- Support for inverted usage (Opened more than closed)