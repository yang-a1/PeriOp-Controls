# temperature_sensor_backend.py
import time
import random

# Try to import Blinka + DHT on a Pi; fall back to a desktop mock.
try:
    import board
    import adafruit_dht
    _ON_PI = hasattr(board, "D4")  # crude but effective
except Exception:
    board = None
    adafruit_dht = None
    _ON_PI = False

_dht = None
_last_ok = None
_last_ts = 0.0
_MIN_PERIOD = 2.2   # seconds between reads (give it some margin)

def _init_dht():
    global _dht
    if _ON_PI and _dht is None:
        try:
            # use_pulseio=False is recommended on Raspberry Pi
            _dht = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        except Exception as e:
            print(f"[ERROR] DHT22 init failed: {e}")
            _dht = None

def get_temperature():
    """
    Returns a string like '22.3 C'.
    On Pi: reads real sensor (rate-limited, with caching).
    Off Pi: returns a simulated stable-ish value for UI.
    """
    global _last_ok, _last_ts

    now = time.monotonic()

    # Desktop / non-Pi fallback (simulate a believable temp)
    if not _ON_PI:
        if _last_ok is None:
            _last_ok = round(22.0 + random.uniform(-0.3, 0.3), 1)
        else:
            # small random walk
            _last_ok = round(_last_ok + random.uniform(-0.05, 0.05), 1)
        return f"{_last_ok:.1f} C"

    # On Pi: ensure sensor object exists
    if _dht is None:
        _init_dht()
        if _dht is None:
            return "--.- C"

    # Respect the min read period
    if now - _last_ts < _MIN_PERIOD:
        return f"{_last_ok:.1f} C" if _last_ok is not None else "--.- C"

    # Try a read
    try:
        temp_c = _dht.temperature
        _last_ts = now
        if temp_c is None:
            # Keep last good value if available
            return f"{_last_ok:.1f} C" if _last_ok is not None else "--.- C"
        # Sanity clamp (optional)
        if -20.0 <= temp_c <= 80.0:
            _last_ok = float(f"{temp_c:.1f}")
            return f"{_last_ok:.1f} C"
        else:
            return f"{_last_ok:.1f} C" if _last_ok is not None else "--.- C"
    except RuntimeError:
        # Common transient error; don’t spam logs, just reuse last
        _last_ts = now
        return f"{_last_ok:.1f} C" if _last_ok is not None else "--.- C"
    except Exception as e:
        # If you want to see hard errors:
        print(f"[ERROR] DHT22 read failed: {e}")
        _last_ts = now
        return f"{_last_ok:.1f} C" if _last_ok is not None else "--.- C"