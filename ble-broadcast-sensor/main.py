# -------------------------------------------------------------------------
# BroadcastNet sensor for BME280.
#
# Adapted from example: ble_broadcastnet_multisensor.py
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
import board
from adafruit_bme280 import advanced as adafruit_bme280
import adafruit_ble_broadcastnet

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

i2c = board.I2C()

#BME280 sensor:
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,address=0x76)
bme280.mode                 = adafruit_bme280.MODE_NORMAL
bme280.standby_period       = adafruit_bme280.STANDBY_TC_500
bme280.iir_filter           = adafruit_bme280.IIR_FILTER_X16
bme280.overscan_pressure    = adafruit_bme280.OVERSCAN_X16
bme280.overscan_humidity    = adafruit_bme280.OVERSCAN_X1
bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X2

altitude_at_location = 525
alt_fac = pow(1.0-altitude_at_location/44330.0, 5.255)

while True:
  measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()
  measurement.temperature       = bme280.temperature
  measurement.relative_humidity = bme280.humidity
  measurement.pressure          = bme280.pressure/alt_fac
  print(measurement)
  adafruit_ble_broadcastnet.broadcast(measurement)
  time.sleep(10)
