from pathlib import Path
import json

BASE = Path(__file__).parent.parent
EVENTS = BASE / "data" / "events.json"
OUTPUT = Path.home() / "mini-siem" / "data" / "web_security_events.json"

events = json.loads(EVENTS.read_text())

OUTPUT.write_text(
    json.dumps(events, indent=2)
)

print(f"Exported events: {len(events)}")
print(f"Output: {OUTPUT}")
