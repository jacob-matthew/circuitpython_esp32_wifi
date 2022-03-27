# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# adafruit_circuitpython_adafruitio usage with an esp32spi_socket
from random import randint
import board
import busio
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
import hd44780

# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials. DO NOT share that file or commit it into Git or other
# source control.
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    display.write("WiFi secrets are kept in secrets.py, please add them there!")
    time.sleep(2)
    display.clear()
    raise

# If you are using a board with pre-defined ESP32 Pins:
#esp32_cs = DigitalInOut(board.ESP_CS)
#esp32_ready = DigitalInOut(board.ESP_BUSY)
#esp32_reset = DigitalInOut(board.ESP_RESET)

# If you have an externally connected ESP32:
esp32_cs = DigitalInOut(board.D13)
esp32_ready = DigitalInOut(board.D11)
esp32_reset = DigitalInOut(board.D12)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

display.write("Connecting to AP...")
time.sleep(2)
display.clear()
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        display.write("could not connect to AP, retrying: ", e)
        time.sleep(2)
        display.clear()
        continue
display.write("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
time.sleep(2)
display.clear()

socket.set_interface(esp)
requests.set_socket(socket, esp)

# Set your Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)

try:
    # Get the 'temperature' feed from Adafruit IO
    temperature_feed = io.get_feed("temperature")
except AdafruitIO_RequestError:
    # If no 'temperature' feed exists, create one
    temperature_feed = io.create_new_feed("temperature")

# Send random integer values to the feed
random_value = randint(0, 50)
display.write("Sending {0} to temperature feed...".format(random_value))
time.sleep(2)
display.clear()
io.send_data(temperature_feed["key"], random_value)
display.write("Data sent!")
time.sleep(2)
display.clear()

# Retrieve data value from the feed
display.write("Retrieving data from temperature feed...")
time.sleep(2)
display.clear()
received_data = io.receive_data(temperature_feed["key"])
display.write("Data from temperature feed: ", received_data["value"])
time.sleep(2)
display.clear()
display.write(ipaddress)
time.sleep(3)

