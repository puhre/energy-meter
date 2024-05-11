from energy_meter import mqtt
from energy_meter.util import config, log
from machine import UART, Pin
import gc
from energy_meter.han.helpers import create_messages
import array

class Config(config.Config):
    # uart id
    id: int = 1
    baudrate: int = 115200
    # Timeout in ms
    timeout: int = 11000
    # Rx pin
    pin: int = 5

class Han:
    _config: Config
    _com: mqtt.Com
    _run: bool = True
    _uart: UART
    _led: machine.Pin
    

    def __init__(self, led, log: log.Log, config: Config, com: mqtt.Com):
        self._validate_config(config)

        self._config = config
        self._led = led
        self._uart = UART(
            self._config.id, 
            baudrate=self._config.baudrate, 
            invert=UART.INV_RX, 
            rx=Pin(self._config.pin), 
            timeout=self._config.timeout
        )
        self._log = log
        self._com = com

    def _validate_config(self, config: Config):
        if config.pin not in [1, 5, 9, 13, 17]:
            raise conf.InvalidConfig("Invalid RX pin {}".format(config.pin))
        if config.id not in [0, 1]:
            raise conf.InvalidConfig("Invalid id {}".format(config.id))
        if config.pin == 1 and config.id != 0:
            raise conf.InvalidConfig("Invalid port config, RX pin {}, id {}".format(config.pin, config.id))
        if config.pin == 5 and config.id != 1:
            raise conf.InvalidConfig("Invalid port config, RX pin {}, id {}".format(config.pin, config.id))
        if config.pin == 9 and config.id != 1:
            raise conf.InvalidConfig("Invalid port config, RX pin {}, id {}".format(config.pin, config.id))
        if config.pin == 12 and config.id != 0:
            raise conf.InvalidConfig("Invalid port config, RX pin {}, id {}".format(config.pin, config.id))
        if config.pin == 17 and config.id != 0:
            raise conf.InvalidConfig("Invalid port config, RX pin {}, id {}".format(config.pin, config.id))

    def stop(self):
        self._run = False
        self._uart.deinit()

    def _read_block(self, data: bytearray, block_splits: bytearray) -> int:
        n_bytes = 0
        n_blocks = 0
        
        # Read first page
        s = ["!"]
        while s[0] != ord('/'):
            # Wait until beginning of block
            _s = self._uart.readline()
            if _s is not None:
                self._log.debug("Got block: {}", _s)
                s = _s
            else:
                self._log.debug("Timed out waiting for block")
            


        self._log.debug("Reading data from HAN port")
        self._led.on()

        # Append data
        data[n_bytes:n_bytes+len(s)] = s
        # Move pointer
        n_bytes += len(s)
        # Note block start and end
        block_splits[0] = len(s)
        n_blocks = 1

        # Read until the end of block
        while True:
            # Read new line
            s = self._uart.readline()
            if s is None:
                self._log.error("Timed out waiting for data, throwing away block")
                n_bytes = 0
                n_blocks = 0
                break

            if s[0] == ord('!'):
                # Final block is here, TODO calculate validity
                # https://hanporten.se/svenska/protokollet/
                break

            if (n_bytes + len(s)) > len(data):
                # Two much data
                self._log.error("Data overflow, dropping data blocks")
                n_bytes = 0
                n_blocks = 0
                break
            
            if (n_blocks + 1) > len(block_splits):
                # Two Many blocks
                self._log.error("Data overflow, dropping data blocks")
                n_bytes = 0
                n_blocks = 0
                break

            # Append data
            data[n_bytes:n_bytes+len(s)] = s
            # Move pointer
            n_bytes += len(s)

            # Note block end
            block_start = block_splits[n_blocks-1]
            block_end = block_start + len(s)
            block_splits[n_blocks] = block_end
            n_blocks += 1

        self._led.off()
        self._log.debug("Read {} bytes", n_bytes)

        gc.collect()  
        return n_bytes, n_blocks

    def read_data(self):
        self._log.info("Starting to listen for messages from HAN port")
        while self._run:
            
            buf = bytearray(1024)
            mv = memoryview(buf)
            block_splits = array.array('i', (0 for _ in range(32)))
            mv_block_splits = memoryview(block_splits)
            n_bytes, n_blocks = self._read_block(mv, mv_block_splits)
            if n_bytes:
                create_messages(self._com, mv[:n_bytes], mv_block_splits[:n_blocks])
        self._log.info("Exiting HAN loop")
                
                
