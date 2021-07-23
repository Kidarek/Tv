from pylgtv import WebOsClient
from wakeonlan import send_magic_packet
import time

send_magic_packet("30:B1:B5:19:39:14")

time.sleep(2)
wc = WebOsClient('192.168.1.134')

for i in range(10):
    try:
        wc.launch_app('netflix')
        break
    except:
        time.sleep(.5)
