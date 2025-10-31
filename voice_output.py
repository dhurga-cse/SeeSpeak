import pyttsx3, threading, queue

_engine = pyttsx3.init()
_engine.setProperty("rate", 225)
_engine.setProperty("volume", 1.0)

_q = queue.Queue()

def _worker():
    while True:
        item = _q.get()
        if item is None:
            break
        try:
            _engine.say(item)
            _engine.runAndWait()
        except Exception:
            pass
        _q.task_done()

_thread = threading.Thread(target=_worker, daemon=True)
_thread.start()

def speak(text: str):
    if text:
        while not _q.empty():
            try:
                _q.get_nowait()
            except Exception:
                pass
        _q.put(text)

def set_voice(rate=None, volume=None):
    if rate is not None:
        _engine.setProperty("rate", int(rate))
    if volume is not None:
        _engine.setProperty("volume", float(volume))

def shutdown():
    _q.put(None)
