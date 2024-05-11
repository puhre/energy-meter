import time
import machine
import config
from energy_meter.mqtt import communication
from energy_meter.han import hancom
from energy_meter.hass.hass import SendConfigMessages
from energy_meter.util import log as _log


import _thread

ALIVE_INTERVAL = 10
global TICKS_0
TICKS_0 = time.ticks_ms()

def start():
   led = machine.Pin("LED", machine.Pin.OUT)
   
   _log.ConfigLogger(config.Log)
   log = _log.get_logger()
   com = communication.Com(led, log, config.COM)

   # Connect to WiFi and MQTT
   if not com.connect():
      log.error("Restarting due to error")
      machine.soft_reset()

   log._sync_clock()
   log.debug("Starting Threads")
   com.run_in_background()
   log.debug("Here")

   try:
      SendConfigMessages(com)
      com.schedule_health(10000)
      com.schedule_uptime(10000)
   except Exception as e:
      com.stop()
      log.error("Something unknown happened: {}", str(e))
      time.sleep(1)
      machine.soft_reset()

   try:
      han = hancom.Han(led, log, config.HAN, com)
   except Exception as e:
      log.error("Failed setting up HAN communication: {}", str(e))
      com.stop()
      machine.soft_reset()

   try:
      han.read_data()
   except KeyboardInterrupt:
      log.info("Got Ctr+c")

   com.stop()
   han.stop()

   time.sleep(1)
   _thread.exit()
   
   log.info("Exiting")
   
   machine.soft_reset()


if __name__ == "__main__":
   start()
