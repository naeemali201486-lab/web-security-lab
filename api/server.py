from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import html
from pathlib import Path
from datetime import datetime

HOST = "127.0.0.1"
PORT = 9300


class Handler(BaseHTTPRequestHandler):

    def log_security_event(self, event, level, details):
        events_file = Path(__file__).parent.parent / "data" / "runtime_events.json"

        try:
            events = json.loads(events_file.read_text()) if events_file.exists() else []
        except json.JSONDecodeError:
            events = []

        events.append({
            "timestamp": datetime.now().astimezone().isoformat(),
            "level": level,
            "event": event,
            "details": details
        })

        events_file.write_text(json.dumps(events, indent=2))

    def send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode()

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))

        # Basic security headers for the local practice API
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'none'")
        self.send_header("Cache-Control", "no-store")

        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html, status=200):
        body = html.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.send_json({
                "service": "web-security-practice-lab",
                "status": "ok",
                "endpoints": [
                    "/api/health",
                    "/api/search?q=test"
                ]
            })

        elif parsed.path == "/api/health":
            self.send_json({
                "status": "ok",
                "service": "web-security-practice-lab"
            })

        elif parsed.path == "/api/search":
            query = parse_qs(parsed.query).get("q", [""])[0]

            self.send_json({
                "query": query,
                "result": f"Practice result for: {query}"
            })

        elif parsed.path == "/training/unsafe":
            value = parse_qs(parsed.query).get("q", [""])[0]

            if "<" in value or ">" in value:
                self.log_security_event(
                    "html_input_detected",
                    "WARN",
                    {
                        "endpoint": "/training/unsafe",
                        "method": "GET",
                        "input_length": len(value)
                    }
                )

            page = f"""<!doctype html>
<html>
<head><title>Unsafe Reflection Demo</title></head>
<body>
<h2>Unsafe Reflection Demo</h2>
<p>Input is inserted directly into HTML:</p>
<div>{value}</div>
</body>
</html>"""

            self.send_html(page)

        elif parsed.path == "/training/safe":
            value = parse_qs(parsed.query).get("q", [""])[0]
            safe_value = html.escape(value)

            page = f"""<!doctype html>
<html>
<head><title>Safe Reflection Demo</title></head>
<body>
<h2>Safe Reflection Demo</h2>
<p>Input is HTML-escaped before output:</p>
<div>{safe_value}</div>
</body>
</html>"""

            self.send_html(page)

        elif parsed.path == "/api/training":
            self.send_json({
                "service": "training-endpoint",
                "purpose": "local-security-practice",
                "status": "enabled"
            })

        else:
            self.send_json({
                "error": "Not found"
            }, 404)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)

    print(
        f"Web Security Practice Lab running on "
        f"http://{HOST}:{PORT}"
    )

    server.serve_forever()
