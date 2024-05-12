from energy_meter.hass import hass
import json
import time
from datetime import datetime as dt

def ticks_ms():
    return int(dt.timestamp(dt.now()))
time.ticks_ms = ticks_ms

def test_HealthMessages():
    m = hass.HassMqttMessageHealth()
    
    assert m.get_payload() == b"online"
    assert m.get_topic() == b"homeassistant/sensor/aabbccdd1122/health"
    
    config_msg = hass.HassMqttMessageHealth.get_config_message()
    assert config_msg.get_topic() == b"homeassistant/sensor/aabbccdd1122/health/config"
    config = json.loads(config_msg.get_payload())
    assert "~" in config
    assert config["~"] == "homeassistant/sensor/aabbccdd1122"
    assert "state_topic" in config
    assert config["state_topic"] == "~/health"
    assert "sw" in config
    assert "device_class" in config
    assert config["device_class"] == "enum"
    assert "options" in config
    assert config["options"] == ["online", "offline"]


def test_UptimeMessages():
    m = hass.HassMqttMessageUptime()
    
    assert int(m.get_payload().decode("utf-8")) > 0
    assert m.get_topic() == b"homeassistant/sensor/aabbccdd1122/uptime"
    
    config_msg = hass.HassMqttMessageUptime.get_config_message()
    assert config_msg.get_topic() == b"homeassistant/sensor/aabbccdd1122/uptime/config"
    config = json.loads(config_msg.get_payload())
    assert "~" in config
    assert config["~"] == "homeassistant/sensor/aabbccdd1122"
    assert "state_topic" in config
    assert config["state_topic"] == "~/uptime"
    assert "sw" in config
    assert "device_class" in config
    assert config["device_class"] == None
    assert "state_class" in config
    assert config["state_class"] == "total_increasing"
