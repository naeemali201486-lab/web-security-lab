import urllib.request

URL = "http://127.0.0.1:9300/api/health"

EXPECTED = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Content-Security-Policy": "default-src 'none'",
    "Cache-Control": "no-store",
}

print("=== SECURITY HEADERS TEST ===")

passed = 0
failed = 0

try:
    with urllib.request.urlopen(URL, timeout=3) as response:
        headers = response.headers

        for name, expected in EXPECTED.items():
            actual = headers.get(name)

            if actual == expected:
                print(f"[PASS] {name}: {actual}")
                passed += 1
            else:
                print(f"[FAIL] {name}: expected={expected}, actual={actual}")
                failed += 1

except Exception as e:
    print(f"[FAIL] Server request: {e}")
    failed += len(EXPECTED)

print()
print("=== FINAL RESULT ===")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("Overall:", "PASS" if failed == 0 else "CHECK REQUIRED")
