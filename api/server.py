from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

HOST = "127.0.0.1"
PORT = 9300


class Handler(BaseHTTPRequestHandler):

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
