from energy_meter.han.hancom import Config as HanConfig
from energy_meter.mqtt.communication import Config as ComConfig, Credentials, WlanConfig
from energy_meter.util.log import Config as LogConfig

from secrets import wlan_ssid, wlan_psk, mqtt_user, mqtt_password, mqtt_host

HOSTNAME = "HANMeter"
COM = ComConfig(
    mqtt = ComConfig.MqttConfig(
        host=mqtt_host,
        credentials=Credentials(
            user=mqtt_user,
            password=mqtt_password
        ),
        max_len_queue=32
    ),
    wlan = WlanConfig(
        ssid=wlan_ssid,
        psk=wlan_psk
    ),
    hostname=HOSTNAME
)

HAN = HanConfig(
    id=0,
    timeout=10000, # ms
    pin=17
)
Log = LogConfig(
    log_file="/log.txt",
    in_terminal=True,
    to_file=False, # Buggy, keep as false unless historical logs are really needed
    max_file_size=10000,
    log_level = "INFO"
)
