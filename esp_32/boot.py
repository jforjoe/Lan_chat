# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import network
import time

def connect_to_wifi(ssid, password):

  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)

  while not wlan.isconnected():
    print('Connecting to network...')
    time.sleep(1)

  if wlan.isconnected():
    print('Network connected:', wlan.ifconfig())
    return wlan.ifconfig()
  else:
    print("Connection failed!")
    return None

# Replace with your WiFi credentials
ssid = 'Esp'
password = '12345678'

# Attempt WiFi connection and store configuration (if successful)
ip_config = connect_to_wifi(ssid, password)

if ip_config:
  print(f'ESP32 IP configuration: {ip_config}')
else:
  print("Failed to obtain IP configuration.")
