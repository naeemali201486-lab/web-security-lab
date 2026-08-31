from pathlib import Path
import json
import urllib.request

BASE = "http://127.0.0.1:9300"
EVENTS = Path("data/runtime_events.json")

# Start with a clean test event file
EVENTS.write_text("[]")

url = f"{BASE}/training/unsafe?q=%3Cb%3EHELLO%3C%2Fb%3E"

print("=== RUNTIME DETECTION TEST ===")

try:
    with urllib.request.urlopen(url, timeout=3) as response:
        print(f"[PASS] Training request -> HTTP {response.status}")
except Exception as e:
    print(f"[FAIL] Training request -> {e}")
    raise SystemExit(1)

events = json.loads(EVENTS.read_text())

matches = [
    event for event in events
    if event.get("event") == "html_input_detected"
    and event.get("details", {}).get("endpoint") == "/training/unsafe"
]

if matches:
    print("[PASS] html_input_detected event generated")
    print("[PASS] Detection pipeline working")
    raise SystemExit(0)

print("[FAIL] Expected security event not found")
raise SystemExit(1)
