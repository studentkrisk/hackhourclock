from machine import Pin,SPI,PWM,reset
import utime, requests, network, _thread

print("starting!")
MOSI = 11
SCK = 10    
RCLK = 9
ssid = ""
password = ""
with open("wifisettings.txt", "r") as f:
    ssid, password = f.read().split("\n")

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        utime.sleep(1)
    print(wlan.ifconfig())

class LED_8SEG():
    def __init__(self):
        self.rclk = Pin(RCLK,Pin.OUT)
        self.rclk(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.SEG8 = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71]
        self.to_write = [self.SEG8[0], self.SEG8[0], self.SEG8[0], self.SEG8[0]]
        self.loading = True
        _thread.start_new_thread(self.write, ())
    def write_cmd(self, Reg, Seg):    
        self.rclk(1)
        self.spi.write(bytearray([Reg]))
        self.spi.write(bytearray([Seg]))
        self.rclk(0)
        utime.sleep(0.002)
        self.rclk(1)
    def write(self):
        while (1):
            self.write_cmd(0XFE,self.to_write[0])
            self.write_cmd(0XFD,self.to_write[1])
            self.write_cmd(0XFB,self.to_write[2])
            self.write_cmd(0XF7,self.to_write[3])



LED = LED_8SEG()

connect()
req = requests.get("https://hackhour.hackclub.com/api/clock/U06MGGA9XM1")
time = int(req.text)

lasttime = utime.time()*1000
while(1):
    time -= utime.time()*1000 - lasttime
    lasttime = utime.time()*1000
    min = time//1000//60
    sec = (time//1000)%60
    LED.to_write = [LED.SEG8[min//10], LED.SEG8[min%10]|0x80, LED.SEG8[sec//10], LED.SEG8[sec%10]]
    # LED.to_write = [0b10000000, 0b01000000, 0b00100000, 0b00010000]
    utime.sleep(0.1)