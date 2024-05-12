import machine
import json
from energy_meter import __VERSION__

HASS_CONFIG_JSON = """\
{{\
"~":"{base_topic}",\
"name":"HANPorter-{topic}",\
"state_topic":"~/{topic}",\
"unit_of_measurement":"{unit}",\
"unique_id":"{sn}-{topic}",\
"device_class":"{device_class}",\
"state_class":"{state_class}",\
"sw":"{version}",\
"url":"https://github.com/puhre/energy-meter",\
"mf":"puhre-engineering",\
"mdl":"v1",\
"hw":"v1",\
"sa":"energy-meter",\
"sn":"{sn}",\
"expire_after":"600",\
"avty_t":"~/{health_topic}",\
"value_template":"{{{{ value | float }}}}",\
"payload_available":"online",\
"payload_not_available":"offline"\
}}\
"""
def create_config_json(
    base_topic: str,
    topic: str,
    unit: str,
    serial_number: str,
    device_class: str,
    state_class: str,
    version: str,
    health_topic: str,
    **kwargs
    ) -> str:
        _c = {
            "~": base_topic,
            "name":"HANPorter-%s" % topic,
            "state_topic":"~/%s" % topic,
            "unit_of_measurement": unit,
            "unique_id":"%s-%s" % (serial_number, topic),
            "device_class": device_class,
            "state_class": state_class,
            "sw": version,
            "url":"https://github.com/puhre/energy-meter",
            "mf":"puhre-engineering",
            "mdl":"v1",
            "hw":"v1",
            "sa": "energy-meter",
            "sn": serial_number,
            "expire_after":"600",
            "avty_t":"~/%s" % health_topic,
            "payload_available":"online",
            "payload_not_available":"offline",
        }
        for k in kwargs:
            _c[k] = kwargs[k]
        return json.dumps(_c, separators=(",",":"))

DeviceClassEnergy = "energy"
DeviceClassApparentEnergy = "apparent-energy"
DeviceClassPower = "power"
DeviceClassApparentPower = "apparent-power"
