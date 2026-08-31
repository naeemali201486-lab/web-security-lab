import urllib.request

BASE = "http://127.0.0.1:9300"
PAYLOAD = "%3Cb%3EHELLO%3C%2Fb%3E"

tests = [
    (
        "Unsafe endpoint reflects raw HTML",
        f"{BASE}/training/unsafe?q={PAYLOAD}",
        "<div><b>HELLO</b></div>",
    ),
    (
        "Safe endpoint escapes HTML",
        f"{BASE}/training/safe?q={PAYLOAD}",
        "<div>&lt;b&gt;HELLO&lt;/b&gt;</div>",
    ),
]

passed = 0
failed = 0

print("=== OUTPUT ENCODING SECURITY TEST ===")

for name, url, expected in tests:
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            body = response.read().decode("utf-8")

        if expected in body:
            print(f"[PASS] {name}")
            passed += 1
        else:
            print(f"[FAIL] {name}")
            failed += 1

    except Exception as e:
        print(f"[FAIL] {name}: {e}")
        failed += 1

print()
print("=== FINAL RESULT ===")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("Overall:", "PASS" if failed == 0 else "CHECK REQUIRED")
