#!/usr/bin/python3
# -------------------------------------------------------------------------
# Read sensor-data of BME280 via nordic-uart.
#
# Adapted from ble_eval_client.py
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/ble-playground
#
# -------------------------------------------------------------------------

# SPDX-FileCopyrightText: 2020 Dan Halbert for Adafruit Industries
# SPDX-License-Identifier: MIT

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart_connection = None

while True:
  if not uart_connection:
    print("Trying to connect...")
    for adv in ble.start_scan(ProvideServicesAdvertisement):
      if UARTService in adv.services and adv.complete_name == "BME280_Sensor":
        uart_connection = ble.connect(adv)
        print("Connected")
        break
    ble.stop_scan()

    if uart_connection and uart_connection.connected:
      uart_service = uart_connection[UARTService]
      while uart_connection.connected:
        data = uart_service.readline().decode("utf-8")
        if data:
          print(data,end='')
