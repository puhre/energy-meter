from energy_meter.util.message import Message
import machine
from energy_meter.hass.hass_config import (
    create_config_json,
)
import json
import time
from energy_meter.mqtt.communication import Com
from energy_meter import __VERSION__
from energy_meter.util import log

_OBJECT_ID = machine.unique_id().hex()
_HASS_PREFIX = "homeassistant/sensor"

class HassMqttMessage(Message):
    _TOPIC = "unset"
    _UNIT = "unset"
    _DEVICE_CLASS = "unset"
    _SATE_CLASS = "measurement"
    _CONFIG = "{}"
    _EXTRA_CONFIG = {
       "value_template": "{{value | float}}"
    }

    def __init__(self, payload: bytes):
        super().__init__(("%s/%s/%s" % (_HASS_PREFIX, _OBJECT_ID, self._TOPIC)).encode(), payload)
    
    @classmethod
    def get_config_message(cls):
        _CONFIG = create_config_json(
            base_topic=("%s/%s" % (_HASS_PREFIX, _OBJECT_ID)),
            topic=cls._TOPIC,
            unit=cls._UNIT,
            device_class=cls._DEVICE_CLASS,
            state_class=cls._SATE_CLASS,
            version=__VERSION__,
            serial_number=_OBJECT_ID,
            health_topic=HassMqttMessageHealth._TOPIC,
            **cls._EXTRA_CONFIG)
        return Message(("%s/%s/%s/%s" % (_HASS_PREFIX, _OBJECT_ID, cls._TOPIC, "config")).encode(), _CONFIG.encode(), True)

class HassMqttMessageHealth(HassMqttMessage):
    _TOPIC = "health"
    _UNIT = ""
    _DEVICE_CLASS = "enum"
    _EXTRA_CONFIG = {
        "options": ["online", "offline"]
    }
    
    def __init__(self):
        super().__init__(b"online")

class HassMqttMessageUptime(HassMqttMessage):
    _TOPIC = "uptime"
    _UNIT = ""
    _DEVICE_CLASS = None
    _SATE_CLASS = "total_increasing"
    
    def __init__(self):
        # TODO: diff with t0
        super().__init__(str(time.ticks_ms()).encode("utf-8"))

# class HassMqttMessageConfig(Message):
#     _PAYLOAD = json.dumps(HASS_CONFIG)
    
#     def __init__(self):
#         super(self._PAYLOAD)

class HassMqttMessageDate(HassMqttMessage):
    # OBIS	    Beskrivning	                            Kommentar	            Exempel-värde
    # 0-0.1.0.0	Datum och tid	                        Formatet YYMMDDhhmmssX	210217184019W
    _TOPIC = "date"
    _UNIT = ""
    _DEVICE_CLASS = "date"

## Energy ##
class HassMqttMessageActiveEnergyOut(HassMqttMessage):
    # OBIS	    Beskrivning	                            Kommentar	            Exempel-värde
    # 1-0:1.8.0	Mätarställning Aktiv Energi Uttag		                        00006678.394*kWh
    _TOPIC = "active-energy-out"
    _UNIT = "kWh"
    _DEVICE_CLASS = "energy"
    _SATE_CLASS = "total_increasing"

class HassMqttMessageActiveEnergyIn(HassMqttMessage):
    # OBIS	    Beskrivning	                            Kommentar	            Exempel-värde
    # 1-0:2.8.0	Mätarställning Aktiv Energi Inmatning		                    00000000.000*kWh
    _TOPIC = "active-energy-in"
    _UNIT = "kWh"
    _DEVICE_CLASS = "energy"
    _SATE_CLASS = "total_increasing"
    
class HassMqttMessageReactiveEnergyIn(HassMqttMessage):
    # OBIS	    Beskrivning	                            Kommentar	            Exempel-värde
    # 1-0.3.8.0	Mätarställning Rektiv Energi Inmatning		                    00000000.000*kWh
    _TOPIC = "reactive-energy-in"
    _UNIT = "varh"
    _DEVICE_CLASS = "reactive_energy"
    _SATE_CLASS = "total_increasing"
    
class HassMqttMessageReactiveEnergyOut(HassMqttMessage):
    # OBIS	    Beskrivning	                            Kommentar	            Exempel-värde
    # 1-0.4.8.0	Mätarställning Rektiv Energi Uttag   		                    00000000.000*kWh
    _TOPIC = "reactive-energy-out"
    _UNIT = "varh"
    _DEVICE_CLASS = "reactive_energy"
    _SATE_CLASS = "total_increasing"


## Power ##
class HassMqttMessageActivePowerOut(HassMqttMessage):
    # OBIS	    Beskrivning	                            Kommentar	            Exempel-värde
    # 1-0:1.7.0	Aktiv Effekt Uttag	                    Momentan trefaseffekt	0001.727*kW
    _TOPIC = "active-power-out"
    _UNIT = "kW"
    _DEVICE_CLASS = "power"

class HassMqttMessageActivePowerIn(HassMqttMessage):
    # OBIS	    Beskrivning	                            Kommentar	            Exempel-värde
    # 1-0:1.7.0	Aktiv Effekt Inmatning                  Momentan trefaseffekt	0000.000*kW
    _TOPIC = "active-power-in"
    _UNIT = "kW"
    _DEVICE_CLASS = "power"

class HassMqttMessageReactivePowerOut(HassMqttMessage):
    # OBIS	    Beskrivning	                            Kommentar	            Exempel-värde
    # 1-0:1.7.0	Reaktiv Effekt Uttag	                Momentan trefaseffekt	0001.727*kvar
    _TOPIC = "reactive-power-out"
    _UNIT = "var"
    _DEVICE_CLASS = "reactive_power"

class HassMqttMessageReactivePowerIn(HassMqttMessage):
    # OBIS	    Beskrivning	                            Kommentar	            Exempel-värde
    # 1-0:1.7.0	Reaktiv Effekt Inmatning                Momentan trefaseffekt	0000.000*kvar
    _TOPIC = "reactive-power-in"
    _UNIT = "var"
    _DEVICE_CLASS = "reactive_power"

## Per line ##
# L1
class HassMqttMessageActivePowerOutL1(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:21.7.0    L1 Aktiv Effekt Uttag	            Momentan effekt	        0001.023*kW
    _TOPIC = "active-power-out-l1"
    _UNIT = "kW"
    _DEVICE_CLASS = "power"

class HassMqttMessageActivePowerInL1(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:22.7.0    L1 Aktiv Effekt Inmatning	        Momentan effekt	        0001.023*kW
    _TOPIC = "active-power-in-l1"
    _UNIT = "kW"
    _DEVICE_CLASS = "power"

class HassMqttMessageReactivePowerOutL1(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:23.7.0    L1 Reaktiv Effekt Uttag	            Momentan effekt	        0001.023*kvar
    _TOPIC = "reactive-power-out-l1"
    _UNIT = "var"
    _DEVICE_CLASS = "reactive_power"

class HassMqttMessageReactivePowerInL1(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:24.7.0    L1 Reaktiv Effekt Inmatning	        Momentan effekt	        0001.023*kvar
    _TOPIC = "reactive-power-in-l1"
    _UNIT = "var"
    _DEVICE_CLASS = "reactive_power"

class HassMqttMessageVoltageL1(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:32.7.0	L1 Fasspänning	                    Momentant RMS-värde	    240.3*V
    _TOPIC = "voltage-l1"
    _UNIT = "V"
    _DEVICE_CLASS = "voltage"

class HassMqttMessageCurrentL1(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:31.7.0	L1 Fasström 	                    Momentant RMS-värde	    0004.2*A
    _TOPIC = "current-l1"
    _UNIT = "A"
    _DEVICE_CLASS = "current"

# L2
class HassMqttMessageActivePowerOutL2(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:41.7.0    L2 Aktiv Effekt Uttag	            Momentan effekt	        0001.023*kW
    _TOPIC = "active-power-out-l2"
    _UNIT = "kW"
    _DEVICE_CLASS = "power"

class HassMqttMessageActivePowerInL2(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:42.7.0    L2 Aktiv Effekt Inmatning	        Momentan effekt	        0001.023*kW
    _TOPIC = "active-power-in-l2"
    _UNIT = "kW"
    _DEVICE_CLASS = "power"

class HassMqttMessageReactivePowerOutL2(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:43.7.0    L2 Reaktiv Effekt Uttag	            Momentan effekt	        0001.023*kvar
    _TOPIC = "reactive-power-out-l2"
    _UNIT = "var"
    _DEVICE_CLASS = "reactive_power"

class HassMqttMessageReactivePowerInL2(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:44.7.0    L2 Reaktiv Effekt Inmatning	        Momentan effekt	        0001.023*kvar
    _TOPIC = "reactive-power-in-l2"
    _UNIT = "var"
    _DEVICE_CLASS = "reactive_power"

class HassMqttMessageVoltageL2(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:52.7.0	L2 Fasspänning	                    Momentant RMS-värde	    240.3*V
    _TOPIC = "voltage-l2"
    _UNIT = "V"
    _DEVICE_CLASS = "voltage"

class HassMqttMessageCurrentL2(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:51.7.0	L2 Fasström 	                    Momentant RMS-värde	    0004.2*A
    _TOPIC = "current-l2"
    _UNIT = "A"
    _DEVICE_CLASS = "current"

# L3
class HassMqttMessageActivePowerOutL3(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:61.7.0    L3 Aktiv Effekt Uttag	            Momentan effekt	        0001.023*kW
    _TOPIC = "active-power-out-l3"
    _UNIT = "kW"
    _DEVICE_CLASS = "power"

class HassMqttMessageActivePowerInL3(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:62.7.0    L3 Aktiv Effekt Inmatning	        Momentan effekt	        0001.023*kW
    _TOPIC = "active-power-in-l3"
    _UNIT = "kW"
    _DEVICE_CLASS = "power"

class HassMqttMessageReactivePowerOutL3(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:63.7.0    L3 Reaktiv Effekt Uttag	            Momentan effekt	        0001.023*kvar
    _TOPIC = "reactive-power-out-l3"
    _UNIT = "var"
    _DEVICE_CLASS = "reactive_power"

class HassMqttMessageReactivePowerInL3(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:64.7.0    L3 Reaktiv Effekt Inmatning	        Momentan effekt	        0001.023*kvar
    _TOPIC = "reactive-power-in-l3"
    _UNIT = "var"
    _DEVICE_CLASS = "reactive_power"

class HassMqttMessageVoltageL3(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:72.7.0	L3 Fasspänning	                    Momentant RMS-värde	    240.3*V
    _TOPIC = "voltage-l3"
    _UNIT = "V"
    _DEVICE_CLASS = "voltage"

class HassMqttMessageCurrentL3(HassMqttMessage):
    # OBIS	        Beskrivning	                        Kommentar	            Exempel-värde
    # 1-0:71.7.0	L3 Fasström 	                    Momentant RMS-värde	    0004.2*A
    _TOPIC = "current-l3"
    _UNIT = "A"
    _DEVICE_CLASS = "current"

def CreateMessageFromObis(obis: bytes, payload: str):
    if obis == b"0-0:1.0.0":
        return HassMqttMessageDate(payload)
    if obis == b"1-0:1.8.0":
        return HassMqttMessageActiveEnergyOut(payload)
    if obis == b"1-0:2.8.0":
        return HassMqttMessageActiveEnergyIn(payload)
    if obis == b"1-0:3.8.0":
        return HassMqttMessageReactiveEnergyOut(payload)
    if obis == b"1-0:4.8.0":
        return HassMqttMessageReactiveEnergyIn(payload)
    if obis == b"1-0:1.7.0":
        return HassMqttMessageActivePowerOut(payload)
    if obis == b"1-0:2.7.0":
        return HassMqttMessageActivePowerIn(payload)
    if obis == b"1-0:3.7.0":
        return HassMqttMessageReactivePowerOut(payload)
    if obis == b"1-0:4.7.0":
        return HassMqttMessageReactivePowerIn(payload)
    if obis == b"1-0:21.7.0":
        return HassMqttMessageActivePowerOutL1(payload)
    if obis == b"1-0:22.7.0":
        return HassMqttMessageActivePowerInL1(payload)
    if obis == b"1-0:23.7.0":
        return HassMqttMessageReactivePowerOutL1(payload)
    if obis == b"1-0:24.7.0":
        return HassMqttMessageReactivePowerInL1(payload)
    if obis == b"1-0:41.7.0":
        return HassMqttMessageActivePowerOutL2(payload)
    if obis == b"1-0:42.7.0":
        return HassMqttMessageActivePowerInL2(payload)
    if obis == b"1-0:43.7.0":
        return HassMqttMessageReactivePowerOutL2(payload)
    if obis == b"1-0:44.7.0":
        return HassMqttMessageReactivePowerInL2(payload)
    if obis == b"1-0:61.7.0":
        return HassMqttMessageActivePowerOutL3(payload)
    if obis == b"1-0:62.7.0":
        return HassMqttMessageActivePowerInL3(payload)
    if obis == b"1-0:63.7.0":
        return HassMqttMessageReactivePowerOutL3(payload)
    if obis == b"1-0:64.7.0":
        return HassMqttMessageReactivePowerInL3(payload)
    if obis == b"1-0:31.7.0":
        return HassMqttMessageCurrentL1(payload)
    if obis == b"1-0:32.7.0":
        return HassMqttMessageVoltageL1(payload)
    if obis == b"1-0:51.7.0":
        return HassMqttMessageCurrentL2(payload)
    if obis == b"1-0:52.7.0":
        return HassMqttMessageVoltageL2(payload)
    if obis == b"1-0:71.7.0":
        return HassMqttMessageCurrentL3(payload)
    if obis == b"1-0:72.7.0":
        return HassMqttMessageVoltageL3(payload)
    
    print("Failed converting obis")
    return None


def SendConfigMessages(com: Com):
    log.get_logger().info("Sending config messages")
    success = True
    success &= com.send_message(HassMqttMessageHealth.get_config_message())
    success &= com.send_message(HassMqttMessageUptime.get_config_message())
    success &= com.send_message(HassMqttMessageActiveEnergyOut.get_config_message())
    success &= com.send_message(HassMqttMessageDate.get_config_message())
    success &= com.send_message(HassMqttMessageActiveEnergyIn.get_config_message())
    success &= com.send_message(HassMqttMessageReactiveEnergyIn.get_config_message())
    success &= com.send_message(HassMqttMessageReactiveEnergyOut.get_config_message())
    success &= com.send_message(HassMqttMessageActivePowerOut.get_config_message())
    success &= com.send_message(HassMqttMessageActivePowerIn.get_config_message())
    success &= com.send_message(HassMqttMessageReactivePowerOut.get_config_message())
    success &= com.send_message(HassMqttMessageReactivePowerIn.get_config_message())
    success &= com.send_message(HassMqttMessageActivePowerOutL1.get_config_message())
    success &= com.send_message(HassMqttMessageActivePowerInL1.get_config_message())
    success &= com.send_message(HassMqttMessageReactivePowerOutL1.get_config_message())
    success &= com.send_message(HassMqttMessageReactivePowerInL1.get_config_message())
    success &= com.send_message(HassMqttMessageVoltageL1.get_config_message())
    success &= com.send_message(HassMqttMessageCurrentL1.get_config_message())
    success &= com.send_message(HassMqttMessageActivePowerOutL2.get_config_message())
    success &= com.send_message(HassMqttMessageActivePowerInL2.get_config_message())
    success &= com.send_message(HassMqttMessageReactivePowerOutL2.get_config_message())
    success &= com.send_message(HassMqttMessageReactivePowerInL2.get_config_message())
    success &= com.send_message(HassMqttMessageVoltageL2.get_config_message())
    success &= com.send_message(HassMqttMessageCurrentL2.get_config_message())
    success &= com.send_message(HassMqttMessageActivePowerOutL3.get_config_message())
    success &= com.send_message(HassMqttMessageActivePowerInL3.get_config_message())
    success &= com.send_message(HassMqttMessageReactivePowerOutL3.get_config_message())
    success &= com.send_message(HassMqttMessageReactivePowerInL3.get_config_message())
    success &= com.send_message(HassMqttMessageVoltageL3.get_config_message())
    success &= com.send_message(HassMqttMessageCurrentL3.get_config_message())

    
    if not success:
        log.get_logger().error("Failed to send one or more config messages")
