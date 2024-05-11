from energy_meter.hass import hass
from energy_meter.han.helpers import split_block, create_messages
def test_splitting_block():
    tests = [
        {
            "block": b"/ELL5\x5c253833635_A\r\n\r\n",
            "expect": (b"", b"")
        },
        {
            "block": b"0-0:1.0.0(210217184019W)\r\n",
            "expect": (b"0-0:1.0.0", b"210217184019W") 
        },
        {
            "block": b"1-0:1.8.0(00006678.394*kWh)\r\n",
            "expect": (b"1-0:1.8.0", b"00006678.394"),
        },
        {
            "block": b"1-0:2.8.0(00000000.000*kWh)\r\n",
            "expect": (b"1-0:2.8.0", b"00000000.000")
        },
        {
            "block": b"1-0:3.8.0(00000021.988*kvarh)\r\n",
            "expect": (b"1-0:3.8.0", b"00000021.988")
        },
        {
            "block": b"1-0:4.8.0(00001020.971*kvarh)\r\n",
            "expect": (b"1-0:4.8.0", b"00001020.971")
        }
    ]
    
    for test in tests:
        obis, meas = split_block(test["block"])
        e_obis, e_meas = test["expect"]
        assert obis == e_obis, f"Expected obis: {e_obis}, but go {obis}"
        assert meas == e_meas, f"Expected meas: {e_meas}, but go {meas}"


class FakeCom:
    messages = []
    def send_message(self, message):
        self.messages.append(message)
        
def test_create_messages():
    test_data = (
        b"/ELL5\x5c253833635_A\r\n\r\n" # 0
        b"0-0:1.0.0(210217184019W)\r\n" # 1
        b"1-0:1.8.0(00006678.394*kWh)\r\n" # 2
        b"1-0:2.8.0(00000000.000*kWh)\r\n" # 3
        b"1-0:3.8.0(00000021.988*kvarh)\r\n" # 4
        b"1-0:4.8.0(00001020.971*kvarh)\r\n" # 5
        b"1-0:1.7.0(0001.727*kW)\r\n" # 6
        b"1-0:2.7.0(0000.000*kW)\r\n" # 7
        b"1-0:3.7.0(0000.000*kvar)\r\n" # 8
        b"1-0:4.7.0(0000.309*kvar)\r\n" # 9
        b"1-0:21.7.0(0001.023*kW)\r\n" # 10
        b"1-0:41.7.0(0000.350*kW)\r\n" # 11
        b"1-0:61.7.0(0000.353*kW)\r\n" # 12
        b"1-0:22.7.0(0000.000*kW)\r\n" # 13
        b"1-0:42.7.0(0000.000*kW)\r\n" # 14
        b"1-0:62.7.0(0000.000*kW)\r\n" # 15
        b"1-0:23.7.0(0000.000*kvar)\r\n" # 16
        b"1-0:43.7.0(0000.000*kvar)\r\n" # 17
        b"1-0:63.7.0(0000.000*kvar)\r\n" # 18
        b"1-0:24.7.0(0000.009*kvar)\r\n" # 19
        b"1-0:44.7.0(0000.161*kvar)\r\n" # 20
        b"1-0:64.7.0(0000.138*kvar)\r\n" # 21
        b"1-0:32.7.0(240.3*V)\r\n" # 22
        b"1-0:52.7.0(240.1*V)\r\n" # 23
        b"1-0:72.7.0(241.3*V)\r\n" # 24
        b"1-0:31.7.0(004.2*A)\r\n" # 25
        b"1-0:51.7.0(001.6*A)\r\n" # 26
        b"1-0:71.7.0(001.7*A)\r\n!" # 27
    )
    # block_splits = [(0, 20), (21, 46), (47, 75), (76, 104), (105, 135), (136, 166), (167, 190), (191, 214), (215, 240), (241, 266), (267, 291), (292, 316), (317, 341), (342, 366), (367, 391), (392, 416), (417, 443), (444, 470), (471, 497), (498, 524), (525, 551), (552, 578), (579, 599), (600, 620), (621, 641), (642, 662), (663, 683), (684, 704), (705, 705)]
    block_splits = [19, 21, 47, 76, 105, 136, 167, 191, 215, 241, 267, 292, 317, 342, 367, 392, 417, 444, 471, 498, 525, 552, 579, 600, 621, 642, 663, 684, 705]
    
    
    com = FakeCom()
    create_messages(com, test_data, block_splits)
    
    assert(len(com.messages) > 0)
    assert(type(com.messages[0]) != type(None))
    assert(type(com.messages[0]) == hass.HassMqttMessageDate)
    assert(type(com.messages[1]) == hass.HassMqttMessageActiveEnergyOut)
    assert(type(com.messages[2]) == hass.HassMqttMessageActiveEnergyIn)
    assert(type(com.messages[3]) == hass.HassMqttMessageReactiveEnergyOut)
    assert(type(com.messages[4]) == hass.HassMqttMessageReactiveEnergyIn)
    assert(type(com.messages[5]) == hass.HassMqttMessageActivePowerOut)
    assert(type(com.messages[6]) == hass.HassMqttMessageActivePowerIn)
    assert(type(com.messages[7]) == hass.HassMqttMessageReactivePowerOut)
    assert(type(com.messages[8]) == hass.HassMqttMessageReactivePowerIn)
    assert(type(com.messages[9]) == hass.HassMqttMessageActivePowerOutL1)
    assert(type(com.messages[10]) == hass.HassMqttMessageActivePowerOutL2)
    assert(type(com.messages[11]) == hass.HassMqttMessageActivePowerOutL3)
    assert(type(com.messages[12]) == hass.HassMqttMessageActivePowerInL1)
    assert(type(com.messages[13]) == hass.HassMqttMessageActivePowerInL2)
    assert(type(com.messages[14]) == hass.HassMqttMessageActivePowerInL3)
    assert(type(com.messages[15]) == hass.HassMqttMessageReactivePowerOutL1)
    assert(type(com.messages[16]) == hass.HassMqttMessageReactivePowerOutL2)
    assert(type(com.messages[17]) == hass.HassMqttMessageReactivePowerOutL3)
    assert(type(com.messages[18]) == hass.HassMqttMessageReactivePowerInL1)
    assert(type(com.messages[19]) == hass.HassMqttMessageReactivePowerInL2)
    assert(type(com.messages[20]) == hass.HassMqttMessageReactivePowerInL3)
    assert(type(com.messages[21]) == hass.HassMqttMessageVoltageL1)
    assert(type(com.messages[22]) == hass.HassMqttMessageVoltageL2)
    assert(type(com.messages[23]) == hass.HassMqttMessageVoltageL3)
    assert(type(com.messages[24]) == hass.HassMqttMessageCurrentL1)
    assert(type(com.messages[25]) == hass.HassMqttMessageCurrentL2)
    assert(type(com.messages[26]) == hass.HassMqttMessageCurrentL3)
