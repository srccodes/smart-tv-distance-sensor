import wifimgr
from hcsr04 import HCSR04
from machine import Pin,I2C
import ssd1306,time
import urequests

def init():
    i2c = I2C(scl=Pin(19), sda=Pin(18))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)
    sensor = HCSR04(trigger_pin=32, echo_pin=35, echo_timeout_us=1000000)
    
    return oled, sensor

def log(msg, x, y):
    oled.text(msg, x, y)
    oled.show()

def clearDisplay():
    oled.fill(0)

def toggleTvPlayPause():
    try:
        response = urequests.post("http://192.168.0.11:8060/keypress/play")
        print("API Response %s" % response.status_code)
        return response.status_code == 200
    except:
        print("Error !!!")
        log("Error !!!", 0, 40)
        return False
    
         

# Get OLED display & Distance sensor
oled, sensor = init()

# Connect to WIfi
log("Connecting...", 0, 0)
wlan = wifimgr.get_connection()
if wlan is None:
    log("No wifi !!!", 0, 20)
    print("Unable to connect to Wifi")
else:
    log("Connected :-)", 0, 20)
    wifimgr.deactivate_ap()
    print("Deactivated AP mode.")

time.sleep_ms(1000)

prevDistance = -1
isPaused = False

while True:
    currDistance = int(sensor.distance_cm())
    time.sleep_ms(250)
    
    if currDistance != prevDistance:
        print("Distance: %s cm, isPaused: %s" %(currDistance, isPaused))
        clearDisplay()
        log("Dist: %s cm" % currDistance,0, 0)
        
        prevDistance = currDistance
         
        if currDistance < 100:
            if not isPaused and toggleTvPlayPause():
                isPaused = True
        else:
            if isPaused and toggleTvPlayPause():
                isPaused = False
        
        print("TV -> %s" % ("Pause" if isPaused else "Play"))
        log("TV -> %s" % ("Pause" if isPaused else "Play"), 0, 40)
              
