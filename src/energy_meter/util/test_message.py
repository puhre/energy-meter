from energy_meter.util.message import Message, MessageQueue, MessageSchedule
from energy_meter.util import log

log.ConfigLogger(log.Config(to_file=False))

def test_message_pop_push():
    queue = MessageQueue()
    
    success = queue.push(Message(b"first-topic", b"first-payload"))
    assert success, "Message failed to be pushed to queue"
    m = queue.pop(True)
    assert m is not None, "Message should not be None"
    assert m.get_topic() == b"first-topic", "Topic does not match"
    assert m.get_payload() == b"first-payload", "Payload does not match"
    first_timestamp  = m.get_timestamp() 

    queue.push(Message(b"second-topic", b"second-payload"))
    m = queue.pop(True)
    assert m.get_timestamp() > first_timestamp, "Timestamp is not increasing with newer messages"


def test_message_order():
    queue = MessageQueue()
    
    for i in range(0, 5):
        success = queue.push(Message(str(i).encode("utf-8"), str(i).encode("utf-8")))
        assert success, "Message {} failed to be pushed to queue".format(i)

    
    assert queue.pop(True).get_topic() == b"0", "Wrong order of messages"
    assert queue.pop(True).get_topic() == b"1", "Wrong order of messages"
    assert queue.pop(True).get_topic() == b"2", "Wrong order of messages"
    assert queue.pop(True).get_topic() == b"3", "Wrong order of messages"
    assert queue.pop(True).get_topic() == b"4", "Wrong order of messages"

    

def test_overflow():
    queue = MessageQueue(max_len_queue=10)

    
    for i in range(0, 100):
        success = queue.push(Message(str(i).encode("utf-8"), str(i).encode("utf-8")))
        assert success, "Message {} failed to be pushed to queue".format(i)

    messages = []
    for i in range(0, 100):
        m = queue.pop(True)
        if m is not None:
            messages.append(m)
    
    assert len(messages) == 10, "Message queue gets too long"

def test_emptying_queue():
    queue = MessageQueue(max_len_queue=10)

    for i in range(0, 100):
        m = queue.pop(True)
        assert m is None, "Message queue should be empty, got: %s" % str(m)

    for i in range(0, 100):
        success = queue.push(Message(str(i).encode("utf-8"), str(i).encode("utf-8")))
        assert success, "Message {} failed to be pushed to queue".format(i)

    messages = []
    for i in range(0, 100):
        m = queue.pop(True)
        if m is not None:
            messages.append(m)
    
    assert len(messages) == 10, "Message queue gets too long"

def test_many_alternating():
    queue = MessageQueue(max_len_queue=10)

    for i in range(0, 1000):
        success = queue.push(Message(str(i).encode("utf-8"), str(i).encode("utf-8")))
        assert success, "Message {} failed to be pushed to queue".format(i)
        m = queue.pop(True)
        assert m is not None, "Message queue should not be empty"
    
    assert len(queue) == 0, "Message queue is not emptied"

def test_many_in_row():
    queue = MessageQueue(max_len_queue=10)

    for i in range(0, 1000):
        success = queue.push(Message(str(i).encode("utf-8"), str(i).encode("utf-8")))
        assert success, "Message {} failed to be pushed to queue".format(i)

    for i in range(0, 10):
        m = queue.pop(True)
        assert m is not None, "Message queue should not be empty"
        assert m.get_payload() == str(990 + i).encode("utf-8")
    
    assert len(queue) == 0, "Message queue is not emptied"
