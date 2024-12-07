import network
import time
import dht
import max7219
from machine import Pin, SPI, reset
import machine
sensor = dht.DHT11(Pin(16))
spi = SPI(1, baudrate=10000000, polarity=0, phase=0)


#innitalize the Display
spi = SPI(2)
display = max7219.Matrix8x8(spi, Pin(5), 4)

# Replace with your Wi-Fi credentials
SSID = 'WIFI NAME'
PASSWORD = 'WIFI PASWORD'

# Variable Defining wether system is online
online = False

#show attemting conection
display.text('WIFI',0,0)
display.show()
time.sleep(0.1)

def connect_to_wifi(ssid, password):
    global online
    max_attempts = 3
    attempts = 0
    wlan = network.WLAN(network.STA_IF)  # Create a station interface
    wlan.active(True)  # Activate the interface
    display.text('WiFi',0,0)
    display.show()
    time.sleep(0.5)
    while attempts < max_attempts:
        wlan.connect(ssid, password)  # Connect to the Wi-Fi network
        print(f'Attempting to connect to Wi-Fi, attempt {attempts + 1} of {max_attempts}...')

        timeout = 10  # Timeout after 10 seconds
        start_time = time.time()

        while not wlan.isconnected():
            if time.time() - start_time > timeout:
                print('Failed to connect to Wi-Fi on this attempt.')
                break  # Exit the inner loop if timeout occurs
            time.sleep(1)  # Wait for a second before checking again

        if wlan.isconnected():
            print('Connected to Wi-Fi:', wlan.ifconfig())
            time.sleep(1)
            display.fill(0)
            display.show()
            online = True
            return True  # Successful connection

        attempts += 1  # Increment the attempt counter

    print("Failed to connect after 3 attempts. Switching to offline mode.")
    return False  # Return False if all attempts fail

# Call the function to connect to Wi-Fi
try:
    connect_to_wifi(SSID, PASSWORD)
except:
    online = False
    display.fill(0)
    display.text('Er 0',0,0)
    display.show()
    time.sleep(1)
display.show()
    
