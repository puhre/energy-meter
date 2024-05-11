import time
from energy_meter.util import log
import _thread
import heapq

class Message:
    _timestamp: int
    _topic: bytes
    _payload: bytes
    retain: bool
    
    def __init__(self, topic: bytes, payload: bytes, retain: bool = False):
        self._timestamp = time.time_ns()
        self._topic = topic
        self._payload = payload
        self.retain = retain

    def NewHealthMessage():
        return 
    
    def get_payload(self):
        return self._payload

    def get_topic(self):
        return self._topic

    def get_timestamp(self):
        return self._timestamp
    
    def __str__(self):
        if type(self._payload) == memoryview:
            return "{topic=%s, payload=%s}" % (self._topic.decode("utf-8"), bytes(self._payload).decode("utf-8"))
        else:
            return "{topic=%s, payload=%s}" % (self._topic.decode("utf-8"), self._payload.decode("utf-8"))

    def __lt__(self, m):
        return self._timestamp < m.get_timestamp()

class MessageSchedule:
    
    def __init__(self, message_obj: Message, every_ms = 10000, *args, **kwargs):
        self._last_message_ms = time.ticks_ms()
        self._every_ms = every_ms
        self._message_obj = message_obj
        self._args = args
        self._kwargs = kwargs
    def eval(self):
        return (time.ticks_ms() - self._last_message_ms) >= self._every_ms

    def get_message(self):
        self._last_message_ms = time.ticks_ms()
        return self._message_obj(*self._args, **self._kwargs)


class MessageQueue:
    _max_len_queue: int
    _max_lock_wait: float
    _lock: _thread.LockType
    _queue: list

    def __init__(self, max_len_queue: int = 10, max_lock_wait: float = 0.5):
        self._max_len_queue = max_len_queue
        self._max_lock_wait = max_lock_wait
        self._lock = _thread.allocate_lock()
        self._queue = []
    
    def push(self, message: Message) -> bool:
        if len(self) >= self._max_len_queue:
            log.get_logger().warn("Message queue is overflowing, dropping oldest message.")
            self.pop(True)
        
        return self._push(message)
    
    def pop(self, waitflag: int = 0) -> Message:
        return self._pop(waitflag)

    def _push(self, message) -> bool:
        if self._lock.acquire(1, self._max_lock_wait):
            heapq.heappush(self._queue, message)
            self._lock.release()
            return True
        else:
            log.get_logger().warn("Lock could not be acquired, message dropped")
            return False
    
    def _pop(self, waitflag: int) -> Message:
        message = None
        if self._lock.acquire(waitflag, self._max_lock_wait):
            try:
                message = heapq.heappop(self._queue)
            except IndexError:
                pass
            self._lock.release()
        
        return message
    
    def __len__(self) -> int:
        return len(self._queue)

        
        
        
