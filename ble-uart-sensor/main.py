# -------------------------------------------------------------------------
# Send sensor of BME280 via nordic-uart.
#
# Adapted from ble_uart_echo_test.py
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/ble-playground
#
# -------------------------------------------------------------------------

# SPDX-FileCopyrightText: 2020 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
from adafruit_bme280 import advanced as adafruit_bme280
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

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

BLERadio.name = "BME280_Sensor"
BLERadio.tx_power = 60
ble  = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
  print("starting advertisement")
  ble.start_advertising(advertisement)
  while not ble.connected:
    pass
  print("connected")
  while ble.connected:
    measurement = "{0:0.1f},{1:0.1f},{2:0.1f}\n".format(
      bme280.temperature,
      bme280.humidity,
      bme280.pressure/alt_fac
      )
    print(measurement,end='')
    uart.write(measurement.encode("utf-8"))
    time.sleep(10)
