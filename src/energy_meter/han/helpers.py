from energy_meter.hass.hass import CreateMessageFromObis

def create_messages(com, blocks: bytearray, block_splits):
    b_start = 0
    for b_end in block_splits:
        # print("block: {}->{}".format(b_start, b_end))
        obis, payload = split_block(blocks[b_start:b_end])
        message = CreateMessageFromObis(obis, payload)
        if message is not None:
            com.send_message(message)
        b_start = b_end
        
    
def split_block(block: bytearray):
    obis_start, obis_end = 0, 0
    obis_end = False
    payload_start, payload_end = 0, 0
    payload_done = False
    # measurement = b""
    # measurement_done = False
    # unit = b""
    # unit_done = False
    i = 0
    for b in block:
        if b == ord('('):
            obis_end = i
            payload_start = obis_end + 1
        
        if b == ord('*') or b == ord(")"):
            payload_end = i
        # if b == b")":
        #     measurement_done = True
        
        # if b == "\r":
        #     unit_done = True
        
        if obis_end != 0 and payload_end != 0:
            break
        # elif not measurement_done:
        #     measurement += b
        # elif not unit_done:
        #     unit += b

        i += 1
    
    # if obis_end - obis_start < 5:
    #     print("ERRROR: length of obis", obis_end-obis_start)

    return block[obis_start:obis_end], block[payload_start:payload_end]
