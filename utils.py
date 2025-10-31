import time

try:
    import winsound
    _HAS_WINSOUND = True
except Exception:
    _HAS_WINSOUND = False

class Throttle:
    def __init__(self, seconds=3.0):
        self.dt = seconds
        self.last = 0.0
    def ready(self):
        now = time.time()
        if now - self.last >= self.dt:
            self.last = now
            return True
        return False

def beep(freq=1200, dur=120):
    if _HAS_WINSOUND:
        try:
            winsound.Beep(freq, dur)
            return
        except Exception:
            pass
    print("\a", end="", flush=True)
