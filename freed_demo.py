from lib.encoder import Encoder
from machine import Pin
from lib.freed import FreeDWrapper
import socket
import time
import network

UDP_IP = "192.168.11.167"
UDP_PORT = 40000

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('CJF-2.4G', 'cjfszy2002')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


do_connect()

e = Encoder(0, 1, Pin.PULL_UP, min_val = 0, max_val = 100)
def sendFreeD():
    struct = FreeDWrapper(0,0,0,0,0,0,0,0,0)
    bits: 'bytes' = struct.createFreeD().encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    unit = 1000
    while True:
        struct.focus = e.value * unit
        bits: 'bytes' = struct.createFreeD().encode()
        sock.sendto(bits, (UDP_IP, UDP_PORT))
        print("val:", e.value, "Packet", bits.hex(':'), end="\r")
        time.sleep(0.1)

#from lib.microdot import Microdot
# app = Microdot()
# @app.route('/')
# def index(q):
#     return 'Hello, world!'

# app.run(port=80)

sendFreeD()




