#!/usr/bin/python3
# -------------------------------------------------------------------------
# BroadcastNet client (Blinka) for sensor with BME280.
#
# Adapted from example: ble_broadcastnet_blinka_bridge.py
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/ble-playground
#
# -------------------------------------------------------------------------

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import requests
from adafruit_ble.advertising.standard import ManufacturerDataField
import adafruit_ble
import adafruit_ble_broadcastnet


# --- scan for measurement-data   --------------------------------------------

def get_measurement():
  """ scan for measurement-data """

  print("scanning")
  print()

  sequence_numbers = {}
  for measurement in ble.start_scan(
    adafruit_ble_broadcastnet.AdafruitSensorMeasurement,timeout=5):

    reversed_address = [measurement.address.address_bytes[i]
                        for i in range(5, -1, -1)]
    sensor_address = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*reversed_address)

    if sensor_address not in sequence_numbers:
      sequence_numbers[sensor_address] = measurement.sequence_number - 1 % 256
  
    # Skip if we are getting the same broadcast more than once.
    if measurement.sequence_number == sequence_numbers[sensor_address]:
      continue
    number_missed = measurement.sequence_number - sequence_numbers[sensor_address] - 1
    if number_missed < 0:
      number_missed += 256

    # extract attributes
    data = {}
    for attribute in dir(measurement.__class__):
      attribute_instance = getattr(measurement.__class__, attribute)
      if issubclass(attribute_instance.__class__, ManufacturerDataField):
        if attribute != "sequence_number":
          value = getattr(measurement,attribute)
          if value is not None:
            data[attribute] = value

    print(data)
  print("scan done")

# --- main   -----------------------------------------------------------------

ble = adafruit_ble.BLERadio()
client_address = adafruit_ble_broadcastnet.device_address
print("This is BroadcastNet client:", client_address)
print()

while True:
  get_measurement()
  time.sleep(1)

