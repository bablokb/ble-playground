#!/usr/bin/python3

import time
import _bleio
import adafruit_ble
from adafruit_ble.advertising.standard import Advertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService

ble = adafruit_ble.BLERadio()

# --- query device-info   ---------------------------------------------------

def get_details(adv):
  """ try to connecct and query details """

  try:
    conn = ble.connect(adv)
    if DeviceInfoService in conn:
      info_service = conn[DeviceInfoService]
      try:
        manufacturer = info_service.manufacturer
      except AttributeError:
        manufacturer = "(Manufacturer Not specified)"
      try:
        model_number = info_service.model_number
      except AttributeError:
        model_number = "(Model number not specified)"
      print("Device:", manufacturer, model_number)
    else:
      print("No device information.\nServices:")
      for service in conn.values():
        print("  %s" % type(service))
  except _bleio.ConnectionError:
    try:
      conn.disconnect()
    except:
      pass
  


while True:
  print("Scanning...")
  for adv in ble.start_scan(timeout=5):
    print(adv.address,adv.complete_name,repr(adv))
  time.sleep(10)
