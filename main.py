import micropython
from lib.mqtt import MQTTClient



def puback_cb(msg_id):
    print('PUBACK ID = %r' % msg_id)

def suback_cb(msg_id, qos):
    print('SUBACK ID = %r, Accepted QOS = %r' % (msg_id, qos))

def con_cb(connected):
    if connected:
        client.subscribe('/home/sys')
        client.subscribe('/home/temp')

def msg_cb(topic, pay):
    print('Received %s: %s' % (topic.decode("utf-8"), pay.decode("utf-8")))
    if pay == b'reboot' and topic == b'/home/sys':
        display.text('BOOT',0,0)
        display.show()
        time.sleep(1)
        machine.reset()
    elif pay == b'temp' and topic == b'/home/temp':
        sensor.measure()
        time.sleep(0.5)
        try:
            pub_id = client.publish('/home/temp/0v',str(sensor.temperature()), False)
            print('temprature')
        except Exception as e:
            print(e)
    elif pay == b'humid' and topic == b'/home/temp':
        sensor.measure()
        time.sleep(0.5)
        try:
            pub_id = client.publish('/home/temp/0v',str(sensor.humidity()), False)
            print('humidity')
        except Exception as e:
            print(e)
    else:
        print('invalid topic btw')
        print(pay)
  
def displaying():
    try:
        sensor.measure()
    except:
        time.sleep(0.5)
        sensor.measure()
    display.fill(0)
    display.text(f'{sensor.temperature()}c',4,0)
    display.show()
    time.sleep(4)
    display.fill(0)
    display.text(f'{sensor.humidity()}%',4,0)
    display.show()
    time.sleep(3.5)
    
# Replace 'your_username' and 'your_password' with your actual MQTT username and password
username = 'YOUR MQTT USER'
password = 'YOUR MQTT PASSWORD'


client = MQTTClient('192.168.0.49', port=1883)

client.set_connected_callback(con_cb)
client.set_puback_callback(puback_cb)
client.set_suback_callback(suback_cb)
client.set_message_callback(msg_cb)

# Connect with client ID, username, and password
if online == True:
    client.connect('my_client_id', user=username, password=password)

while True:
    displaying()
    time.sleep(1)
