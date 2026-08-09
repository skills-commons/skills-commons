Traceback (most recent call last):
  File "app/worker.py", line 88, in process
    payload = json.loads(msg.body)
  File "/usr/lib/python3.12/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

Happens for about 1 message in 500, in the queue consumer.
