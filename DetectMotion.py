from gpiozero import Button, LED
from signal import pause
from datetime import datetime

from urllib import request
import shutil

camera_address = ""

radar = Button(26) # board37
doorbell = LED(17)

def handle_motion_detected():
  print("Motion detected at " + str(datetime.now()))
  # Ring the doorbell once
  doorbell.blink(on_time=2, off_time=1, n=1, background=True)
  with request.urlopen(camera_address) as response, open(file_name, 'wb') as out_file:
    if response.getStatus() == 200:
      shutil.copyfileobj(response, out_file)

radar.when_deactivated = handle_motion_detected
pause()
