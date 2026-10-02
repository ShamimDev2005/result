import os
import urllib.request
import urllib.parse
import json

# GitHub Actions inputs
exam = os.environ.get("EXAM", "").strip().lower()
year = os.environ.get("YEAR", "").strip()
roll = os.environ.get("ROLL", "").strip()
reg = os.environ.get("REG", "").strip()
board = os.environ.get("BOARD", "").strip()

boards = {
    "1": "Dhaka",
    "2": "Rajshahi",
    "3": "Chittogram",
    "4": "Jashore",
    "5": "Cumilla",
    "6": "Barishal",
    "7": "Sylhet",
    "8": "Dinajpur",
    "9": "Madrasah",
    "10": "Mymensingh",
    "11": "Technical",
    "12": "BOU",
}

if exam not in {"jsc", "ssc", "hsc"}:
    raise SystemExit("ERROR: EXAM must be jsc, ssc, or hsc.")

if not year.isdigit() or len(year) != 4:
    raise SystemExit("ERROR: YEAR must be a 4-digit year.")

if roll and (not roll.isdigit() or len(roll) != 6):
    raise SystemExit("ERROR: ROLL must contain exactly 6 digits.")

if reg and (not reg.isdigit() or len(reg) != 10):
    raise SystemExit("ERROR: REG must contain exactly 10 digits.")

if not roll and not reg:
    raise SystemExit("ERROR: Give at least ROLL or REG.")

if board not in boards:
    raise SystemExit("ERROR: BOARD must be a number from 1 to 12.")

print(f"Exam : {exam.upper()}")
print(f"Year : {year}")
print(f"Board: {boards[board]} ({board})")
print("Fetching result...")

base_url = "http://app.rajshahiboard.gov.bd/esif/ajax/get_result.php"

params = {
    "exam": exam,
    "exam_year": year,
    "roll": roll,
    "reg": reg,
    "board": board,
}

full_url = base_url + "?" + urllib.parse.urlencode(params)

try:
    with urllib.request.urlopen(full_url, timeout=10) as response:
        raw = response.read().decode("utf-8", errors="replace").strip()
except Exception as e:
    raise SystemExit(f"ERROR: Could not fetch result: {e}")

try:
    data = json.loads(raw)
except json.JSONDecodeError:
    print("\nRaw API response:")
    print(raw)
    raise SystemExit("ERROR: API response was not valid JSON.")

print("\n========== RESULT ==========")
print(json.dumps(data, indent=2, ensure_ascii=False))
print("============================")
