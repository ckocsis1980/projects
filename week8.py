import json
import urllib.request


# ── Mock claim data ───────────────────────────────────────────────────────────

# This dictionary stands in for data that would normally come from a real API.
# In production, get_claim_from_api() below would return this structure after
# parsing a live JSON response; here we define it so the fallback has something
# realistic to return.
MOCK_CLAIM = {
    "claim_id": "CLM-2024-00847",
    "patient_name": "Maria Gonzalez",
    "date_of_birth": "1985-03-22",
    "amount": 1250.00,
    "insurance_paid": 975.00,
    "deductible": 275.00,
    "status": "processed"
}


def get_claim_from_api(claim_id):
    """Fetch a claim by ID from the claims API and return it as a dictionary."""

    # Build the endpoint URL by inserting the claim_id into the path.
    # REAL API: replace this base URL with your actual claims system endpoint.
    url = f"https://api.claims-system.com/claims/{claim_id}"

    try:
        # urllib.request.urlopen() sends an HTTP GET request to the URL.
        # If the server responds, we read and decode the raw bytes into a string.
        with urllib.request.urlopen(url) as response:
            raw = response.read().decode("utf-8")

        # json.loads() converts the JSON string the server sent into a Python
        # dictionary, which we return to the caller.
        # REAL API: this return value would be live data from the claims system.
        return json.loads(raw)

    except Exception as e:
        # The real API domain doesn't exist, so the connection will fail.
        # We catch any exception (DNS failure, timeout, HTTP error, etc.),
        # print a notice, and fall back to our local mock data so the rest
        # of the script can still run and demonstrate the JSON parsing logic.
        print(f"[API unavailable: {e}]")
        print("[Falling back to mock claim data]\n")

        # REAL API: remove this fallback once connected to a live endpoint.
        return MOCK_CLAIM


# ── Fetch and display the claim ───────────────────────────────────────────────

# Call our function with a claim ID. With a real API this would hit the network;
# here it falls back to mock data because the domain doesn't exist.
claim = get_claim_from_api("CLM-2024-00847")

# Once loaded, we can access each field using the key name, just like any dictionary.
print("=== Health Insurance Claim ===")
print(f"Claim ID:        {claim['claim_id']}")
print(f"Patient:         {claim['patient_name']}")
print(f"Date of Birth:   {claim['date_of_birth']}")
print(f"Total Amount:    ${claim['amount']:.2f}")
print(f"Insurance Paid:  ${claim['insurance_paid']:.2f}")
print(f"Deductible:      ${claim['deductible']:.2f}")
print(f"Status:          {claim['status'].capitalize()}")

# We can also do calculations using the numeric fields pulled from the JSON.
# This verifies that insurance_paid + deductible equals the total amount billed.
balance_check = claim['insurance_paid'] + claim['deductible']
print(f"\nBalance check: ${claim['insurance_paid']:.2f} + ${claim['deductible']:.2f} = ${balance_check:.2f}")

if balance_check == claim['amount']:
    print("Amounts balance correctly.")
else:
    print("Warning: amounts do not balance.")


# ── Live Weather API Call ─────────────────────────────────────────────────────

# The URL below points to the Open-Meteo API with latitude/longitude for
# Harrisburg, PA. The query parameter current_weather=true tells the API
# to include the current conditions in its response.
url = "https://api.open-meteo.com/v1/forecast?latitude=40.2732&longitude=-76.8867&current_weather=true"

# urllib.request.urlopen() opens the URL and returns a response object.
# The 'with' block ensures the connection is closed automatically when done.
with urllib.request.urlopen(url) as response:
    # response.read() downloads the raw bytes from the server.
    # .decode("utf-8") converts those bytes into a plain Python string.
    raw = response.read().decode("utf-8")

# json.loads() parses the JSON string into a Python dictionary, same as above.
weather_data = json.loads(raw)

# The API returns a nested structure. The current conditions live inside
# the "current_weather" key, which is itself a dictionary.
current = weather_data["current_weather"]

print("\n=== Current Weather — Harrisburg, PA ===")
# temperature is in Celsius by default from Open-Meteo.
# windspeed is in km/h by default.
print(f"Temperature:  {current['temperature']} °C  ({current['temperature'] * 9/5 + 32:.1f} °F)")
print(f"Wind Speed:   {current['windspeed']} km/h")


# ── Claim evaluation logic ────────────────────────────────────────────────────

def evaluate_claim(claim):
    """
    Examine a claim dictionary and return a (flag, patient_responsibility) tuple.

    Flagging rules:
      - DENIED        : status is "denied" — insurance pays nothing, patient owes full amount
      - HIGH VALUE    : total amount exceeds $1,000 — large claims get extra review
      - STANDARD CLAIM: everything else
    Patient responsibility is whatever the insurance did NOT cover.
    """

    amount   = claim["amount"]
    ins_paid = claim["insurance_paid"]
    status   = claim["status"].lower()

    # Rule 1: denied claims — patient is responsible for the entire bill.
    if status == "denied":
        flag = "DENIED"
        patient_responsibility = amount          # insurance paid $0

    # Rule 2: any processed claim over $1,000 is flagged for review.
    elif amount > 1000:
        flag = "HIGH VALUE"
        # Patient owes whatever insurance didn't cover (deductible + any gap).
        patient_responsibility = amount - ins_paid

    # Rule 3: routine claim — no special handling needed.
    else:
        flag = "STANDARD CLAIM"
        patient_responsibility = amount - ins_paid

    return flag, patient_responsibility


# ── Full claim summary report ─────────────────────────────────────────────────

# Fetch the claim through our API function (falls back to mock data if offline).
report_claim = get_claim_from_api("CLM-2024-00847")

# Pass the claim dictionary into evaluate_claim to get the flag and what the
# patient owes. The function returns two values; we unpack them into two variables.
flag, patient_responsibility = evaluate_claim(report_claim)

# Print the complete summary report using the claim fields and evaluated values.
print("\n" + "=" * 45)
print("       CLAIM SUMMARY REPORT")
print("=" * 45)
print(f"  Claim ID     : {report_claim['claim_id']}")
print(f"  Patient      : {report_claim['patient_name']}")
print(f"  Date of Birth: {report_claim['date_of_birth']}")
print(f"  Status       : {report_claim['status'].capitalize()}")
print("-" * 45)
print(f"  Total Billed : ${report_claim['amount']:.2f}")
print(f"  Insurance    : ${report_claim['insurance_paid']:.2f}")
print(f"  Deductible   : ${report_claim['deductible']:.2f}")
print(f"  Patient Owes : ${patient_responsibility:.2f}")
print("-" * 45)
# The flag summarizes the claim category determined by evaluate_claim().
print(f"  FLAG         : *** {flag} ***")
print("=" * 45)
