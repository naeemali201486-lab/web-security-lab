import json
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:9300"

tests = [
    ("Health endpoint", "/api/health", 200),
    ("Training endpoint", "/api/training", 200),
    ("Search endpoint", "/api/search?q=test", 200),
]

passed = 0
failed = 0
results = []

print("=== WEB SECURITY LAB TESTS ===")

for name, path, expected in tests:
    try:
        with urllib.request.urlopen(BASE + path, timeout=3) as response:
            status = response.status
            body = response.read().decode()

        if status == expected:
            print(f"[PASS] {name} -> HTTP {status}")
            passed += 1
            results.append({
                "test": name,
                "status": "PASS",
                "http_status": status
            })
        else:
            print(f"[FAIL] {name} -> HTTP {status}")
            failed += 1

    except Exception as e:
        print(f"[FAIL] {name} -> {e}")
        failed += 1

        results.append({
            "test": name,
            "status": "FAIL",
            "error": str(e)
        })

report = {
    "service": "web-security-practice-lab",
    "tests": results,
    "passed": passed,
    "failed": failed,
    "overall": "PASS" if failed == 0 else "CHECK REQUIRED"
}

with open("reports/security_report.json", "w") as f:
    json.dump(report, f, indent=2)

print()
print("=== FINAL RESULT ===")
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Overall: {report['overall']}")
