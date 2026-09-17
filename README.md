# DJ Deck

This is a personal project that I created to experiment with using physical sensors to control music. The project uses an Arduino to read two distance sensors and a touch sensor, then sends the sensor information to a Python program that controls two music decks.

I also made this project to practice combining hardware and software together and to experiment with real-time sensor-based controls.

## Features

* **Two music decks**
  The project has two separate music decks, Deck A and Deck B. Each deck can have its own audio file, volume, pitch/speed and sound filter settings. The music can also play continuously in a loop.

* **Distance sensor controls**
  Two ultrasonic sensors (sensors that measure distance using sound) are used to control the two decks. If the first sensor detects an object at 20 cm or closer, Deck A is turned on. If the second sensor detects an object at 20 cm or closer, Deck B is turned on. Moving away from the sensor turns the corresponding deck off.

* **Touch sensor control**
  A touch sensor is used to change the pitch and speed of both decks. When the sensor is touched, both decks change to `1.5`, and when it is released, they return to `1.0`.

* **Arduino and Python communication**
  The Arduino constantly reads the sensors and sends their values to the Python program through serial communication (sending data between devices). The information is sent using simple messages such as `US1=15`, `US2=32` and `TOUCH=1`.

* **Sound filtering**
  Each deck uses a filter (a sound control that changes which frequencies can be heard). This allows each deck to have its own filter setting.

## Hardware

The Arduino uses the following connections:

| Component                     | Arduino Pin |
| ----------------------------- | ----------: |
| Ultrasonic Sensor 1 — Trigger |           2 |
| Ultrasonic Sensor 1 — Echo    |           3 |
| Ultrasonic Sensor 2 — Trigger |           4 |
| Ultrasonic Sensor 2 — Echo    |           5 |
| Touch Sensor                  |          11 |

The Arduino measures the distance from both ultrasonic sensors and reads whether the touch sensor is pressed. It then sends the results to the computer about 33 times per second.

## Coding Languages Used

I used **C++** for the Arduino program and **Python** for the main music program.

The Arduino program is responsible for reading the physical sensors and sending their values to the computer. The Python program receives this information and controls the music using the **pyo** audio library.

The Python program also uses **PySerial** (a Python library for communicating with devices through a serial connection) to receive the information from the Arduino.

## Acknowledgements

* [pyo for audio playback and sound processing](https://belangeo.github.io/pyo/)
* [PySerial for communication with the Arduino](https://pyserial.readthedocs.io/)

## Authors

* [@NaderEdward](https://github.com/NaderEdward)
