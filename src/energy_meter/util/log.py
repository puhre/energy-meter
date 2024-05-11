import os
import ntptime
from energy_meter.util import config
import time
import _thread

class Config(config.Config):
    log_file: str = "/log.txt"
    in_terminal: bool = False
    to_file: bool = True
    max_file_size: int = 100000
    max_number_of_files: int = 3
    log_level: str = "WARNING"

class LoggerNotDefined(Exception):
    def __init__(self):
        super().__init__("Logger is not defined")

class LoggerAlreadyDefined(Exception):
    def __init__(self):
        super().__init__("Logger already defined")

class Log:  

    _INFO = "INFO"
    _DEBUG = "DEBUG"
    _WARN = "WARNING"
    _ERROR = "ERROR"

    _LEVELS = {
        _DEBUG: 1,
        _INFO: 2,
        _WARN: 3,
        _ERROR: 4
    }

    _config: Config
    _write_lock = None

    def __init__(self, config: Config):
        self._validate_config(config)
        self._config = config
        self._sync_clock()
        self._write_lock = _thread.allocate_lock()
        if self._write_lock.locked():
            print("Releasing write lock")
            self._write_lock.release()

    def _validate_config(self, conf: Config):
        if conf.log_level not in self._LEVELS:
            raise config.InvalidConfig("%s not a valid config level" % conf.log_level)
        
    
    def _sync_clock(self):
        try:
            ntptime.settime()
        except Exception as e:
            print("Failed setting time, timestamp wont be correct")
        
    def _log(self, level, log_line):
        if self._LEVELS[level] < self._LEVELS[self._config.log_level]:
            return 
        
        t = time.localtime()
        _log_line = "{}:{}:{}-{}-{}-{} - [{}] {}\n".format(t[3], t[4], t[5], t[0], t[1], t[2], level, log_line)
        if self._config.in_terminal:
            print(_log_line, end="")
        if self._config.to_file:
            if self._write_lock.acquire(True, 0.1):
                try:
                    with open(self._config.log_file, 'at') as f:
                        f.write(_log_line)
            
                    if os.stat(self._config.log_file)[6] >= self._config.max_file_size:
                        print("File too large, renaming files")
                        for i in range(self._config.max_number_of_files, 0, -1):
                            try:
                                if i > 1:
                                    os.rename(self._config.log_file + "-" + str(i-1), self._config.log_file + "-" + str(i))
                                else:
                                    os.rename(self._config.log_file, self._config.log_file + "-" + str(i))
                            except Exception:
                                # Ignore if files does not exist yet
                                pass
                except Exception as e:
                    print("Unknown error occurred: %s" % str(e))

                self._write_lock.release()
            else:
                print("Failed acquiring write lock")

    def info(self, log_line, *args):
        self._log(self._INFO, log_line.format(*args))

    def debug(self, log_line, *args):
        self._log(self._DEBUG, log_line.format(*args))

    def error(self, log_line, *args):
        self._log(self._ERROR, log_line.format(*args))

    def warn(self, log_line, *args):
        self._log(self._WARN, log_line.format(*args))

global logger
logger = None

def ConfigLogger(config: Config):
    global logger
    if logger is not None:
        raise LoggerAlreadyDefined()
    logger = Log(config)
    return logger

def get_logger():
    global logger
    if logger is None:
        raise LoggerNotDefined()
    return logger
