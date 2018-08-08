from nanpy import SerialManager
from dsd import (Rack, Dispenser)
from time import sleep
import paho.mqtt.client as mqtt
import requests
import json

host = 'https://dsd-api.herokuapp.com/'
apiSearch = 'api/dispenser/search?name=UTT - Vinculación - Primeros auxilios'
apiDispenser = 'api/dispenser/{}?kits=1'
url = host + apiSearch
dispenser = None


def on_connect(client, userdata, flags, rc):
    print("Connected to broker, result: "+str(rc))
    client.subscribe("/dsd/dispenser/dispense")


def on_message(client, userdata, msg):
    json_data = json.loads(msg.payload.decode("utf-8"))
    print(json_data)
    if 'kit' in json_data:
        kit = json_data['kit']
        rack = dispenser.findRackByKit(kit)
        if rack is not None:
            print('Dispensing...')
            dispenser.dispense(rack)


try:
    connection = SerialManager(device='/dev/ttyACM0')
    print('Connection stabished')
    response = requests.get(url)
    if(response.status_code == 200):
        url = host + apiDispenser
        dispenserId = response.json()['dispenser']['_id']
        print(dispenserId)
        print(url.format(dispenserId))
        response = requests.get(url.format(dispenserId))
        if(response.status_code == 200):
            dispenser = Dispenser(data=response.json(), serial=connection)
            print('dispenser: %s' % dispenser)
            for rack in dispenser.racks:
                print(rack.kit.id)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('test.mosquitto.org', 1883, 60)
    client.loop_forever()
except Exception as e:
    print(e)
