import network
import heapq
import time
import _thread
from umqtt.simple import MQTTClient
from energy_meter.util import config as conf
from energy_meter.util.message import Message, MessageSchedule, MessageQueue
from energy_meter.hass import hass
import machine
    
class WlanConfig(conf.Config):
    ssid: str = ""
    psk: str = ""

class Credentials(conf.Config):
    user: str = ""
    psk: str = ""
class Config(conf.Config):

    class MqttConfig(conf.Config):
        port: int = 1883
        host: str = "192.168.255.255"
        max_len_queue: int = 10
        credentials: Credentials

    mqtt: MqttConfig
    wlan: WlanConfig
    hostname: str
    
class Com:
    
    _message_queue: MessageQueue
    _message_lock = None
    _log = None
    _config: Config
    _hostname: str
    _led: machine.Pin
    _t0 = 0
    def __init__(self, led, log, config: Config):
        self._validate_config(config)
        self._config = config
        self._scheduled_messages = []
        self._message_queue = MessageQueue(max_len_queue=self._config.mqtt.max_len_queue)
        self._log = log
        self._led = led
        self._message_lock = _thread.allocate_lock()
        if self._message_lock.locked():
            self._log.info("Releasing message lock")
            self._message_lock.release()
        self._t0 = time.ticks_ms()

    def _validate_config(self, config: Config):
        if config.wlan.ssid == "" or config.wlan.ssid is None:
            raise conf.InvalidConfig("WLAN SSID is not set")
        if config.wlan.psk == "" or config.wlan.psk is None:
            raise conf.InvalidConfig("WLAN PSK is not set")

    def _setup_wifi(self):
        network.hostname(self._config.hostname)
        wlan = network.WLAN(network.STA_IF)

        self._log.debug("Connecting to {}", self._config.wlan.ssid)
        waitcount = 120
        wlan.active(True)

        try:
            wlan.connect(self._config.wlan.ssid, self._config.wlan.psk)
        except OSError as error:
            self._log.error("Failed connecting to WLAN: %s", str(error))
            return False
        
        waitcount = 120
        while not wlan.isconnected():
            self._log.info("Waiting for WiFi to come online ({})", waitcount)
            waitcount-=1
            time.sleep(0.5)
            self._led.toggle()
            if waitcount <= 0:
                self._led.off()
                self._log.error("Failed setting up WiFi")
                return False
        
        return True
        
    def connect(self) -> bool:
        self._client = MQTTClient(
            self._config.hostname,
            server=self._config.mqtt.host,
            port=self._config.mqtt.port,
            user=self._config.mqtt.credentials.user,
            password=self._config.mqtt.credentials.password
        )
        
        if not self._setup_wifi():
            self._log.error("Failed connecting to WiFi with SSID {}", self._config.wlan.ssid)
            return False

        try:
            self._client.connect()
            self._log.info("Connected over MQTT to {}:{}", self._config.mqtt.host, self._config.mqtt.port)
            return True
        except Exception as e:
            self._log.error("Failed connecting to {}:{}: {}", self._config.mqtt.host, self._config.mqtt.port, str(e))
            return False

    def _add_scheduled_message(self, intervall_ms, message_obj: Message, *args, **kwargs):
        self._scheduled_messages.append(MessageSchedule(message_obj, intervall_ms, *args, **kwargs))

    def schedule_health(self, intervall_ms):
        self._log.debug("Scheduling health message every {} ms", intervall_ms)
        self._add_scheduled_message(intervall_ms, hass.HassMqttMessageHealth)

    def schedule_uptime(self, intervall_ms):
        self._log.debug("Scheduling uptime message every {} ms", intervall_ms)
        self._add_scheduled_message(intervall_ms, hass.HassMqttMessageUptime)

    def _get_alive(self) -> bytes:
        return b"online"
    def _get_uptime(self) -> bytes:
        return str(time.ticks_ms() - self._t0).encode("utf-8")


    def _add_message(self, message) -> bool:
        return self._message_queue.push(message)
            
    def _read_message(self) -> Message:
        return self._message_queue.pop()

    def send_message(self, message: Message) -> bool:
        return self._add_message(message)

    def _send(self, message):
        self._log.debug("Sending message {}", message)
        payload = message.get_payload()
        if type(payload) == memoryview:
            self._client.publish(message.get_topic(), bytes(payload), retain=message.retain)
        else:
            self._client.publish(message.get_topic(), payload, retain=message.retain)

    def stop(self):
        self._run = False

    def run_in_background(self):
        self._run = True
        def _thread_func():
            while self._run: 
                # Add scheduled messages to queue
                for m in self._scheduled_messages:
                    if m.eval():
                        self._log.debug("Scheduled message is due: {}", m.get_message().get_topic())
                        self._add_message(m.get_message())

                # Send messages
                message = self._read_message()
                while message != None:
                    try:
                        self._send(message)
                    except Exception as e:
                        # self._add_message(message)
                        self._log.error("Failed sending message: {}, retrying later", str(e))
                    message = self._read_message()
                    time.sleep_ms(70)

                time.sleep_ms(10)

            self._client.disconnect()
            self._log.info("Exiting communication thread")

        _thread.start_new_thread(_thread_func, ())
