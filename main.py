from machine import Pin,SPI,PWM
import utime, requests, network

ssid = input("ssid> ")
password = input("password> ")

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid)
    while wlan.isconnected() == False:
        print('Waiting for connection..')
        utime.sleep(1)
    # print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

connect()

MOSI = 11
SCK = 10    
RCLK = 9

SEG8Code = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71]
class LED_8SEG():
    def __init__(self):
        self.rclk = Pin(RCLK,Pin.OUT)
        self.rclk(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.SEG8=SEG8Code
    def write_cmd(self, Reg, Seg):    
        self.rclk(1)
        self.spi.write(bytearray([Reg]))
        self.spi.write(bytearray([Seg]))
        self.rclk(0)
        utime.sleep(0.002)
        self.rclk(1)

if __name__=='__main__':
    LED = LED_8SEG()
    req = requests.get("https://hackhour.hackclub.com/api/clock/U06MGGA9XM1")
    print(req)
    while(1):
        LED.write_cmd(0XFE,LED.SEG8[4]|0X80)
        LED.write_cmd(0XFD,LED.SEG8[3]|0X80)
        LED.write_cmd(0XFB,LED.SEG8[2]|0X80)
        LED.write_cmd(0XF7,LED.SEG8[1]|0X80)