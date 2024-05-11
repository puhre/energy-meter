import machine
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

DeviceClassEnergy = "energy"
DeviceClassApparentEnergy = "apparent-energy"
DeviceClassPower = "power"
DeviceClassApparentPower = "apparent-power"
