# Stream Temps 
![Logo](./images/logo_120x120.png "Logo")

Let your viewers know that you are sweating

## Requirements

 * Raspberry Pi 2, 3, or 4 with Raspberry Pi OS. You can find the setup video [here](https://www.youtube.com/watch?v=NAqBgF0swYo).
 * DHT-22 Sensor
 * Python Version `3.7.3+` installed

## Setup
### Hardware

### DHT-22 Sensor
<img src="./images/dht_22.png" width="100" />

* Pin 1: VCC (power supply)
* Pin 2: DATA (data signal)
* Pin 3: not connected
* Pin 4: GND (ground)

### Raspberry Pi Pinout
<img src="./images/raspberry_pi_pinout.png" width="700" />

* Pin 1: VCC 3.3V
* Pin 6: GND
* Pin 7: GPIO 4

### Schematic
<img src="./images/schematic.png" width="400" />

* 10k Resistor between Pin 1 and Pin 2 of the DHT-22
* Wire Pin 1 (VCC) of the DHT-22 to Pin 1 (VCC 3.3V) of the Raspberry Pi
* Wire Pin 2 (DATA) of the DHT-22 to Pin 7 (GPIO 4) of the Raspberry Pi
* Wire Pin 4 (GND) of the DHT-22 to Pin 6 (GND) of the Raspberry Pi

*Raspberry Pi Pinout from: [https://www.raspberrypi.org/documentation/usage/gpio/](https://www.raspberrypi.org/documentation/usage/gpio/)*

### Software

* Download from TODO
* unzip and double click on `run.sh` TODO

## Bundle + Zip with PyInstaller

Bundling has to take place on a Raspberry Pi

```bash
make zip
```

## Command Line

```bash
python3 -m pip install -r requirements.txt
python3 stream_temps.py
```

## Credits
![K0nze Logo](./images/k_logo_30x30.png "Logo") Created by Konstantin (Konze) Lübeck

 * Discord: [discord.k0nze.gg](https://discord.k0nze.org) 
 * Twitch: [twitch.tv/k0nze](https://twitch.tv/k0nze) 
 * Youtube: [youtube.com/k0nze](https://youtube.com/k0nze) 
 * Twitter: [twitter.com/k0nze_gg](https://twitter.com/k0nze_gg) 
 * Instagram: [instagram.com/k0nze.gg](https://instagram.com/k0nze.gg) 
