from energy_meter.hass import hass
import json

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
    assert config["sw"] == "1.0.0"
    assert config["device_class"] == "None"
