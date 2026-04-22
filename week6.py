# A list is an ordered collection of items stored in a single variable.
# Each item here is a dictionary — a collection of key/value pairs using {}.
# Dictionaries let us group related fields together under one claim record.

claims = [
    {"claim_id": "C001", "patient_name": "Alice Johnson",  "amount": 1200.50, "status": "Approved"},
    {"claim_id": "C002", "patient_name": "Brian Smith",    "amount": 3450.00, "status": "Approved"},
    {"claim_id": "C003", "patient_name": "Carol Davis",    "amount": 875.25,  "status": "Denied"},
    {"claim_id": "C004", "patient_name": "David Lee",      "amount": 5600.75, "status": "Approved"},
    {"claim_id": "C005", "patient_name": "Emma Wilson",    "amount": 2100.00, "status": "Denied"},
]

# Counters to track summary totals as we loop.
total_amount = 0
denied_count = 0
high_value_count = 0

# Loop through each claim dictionary and print a summary.
for claim in claims:
    print(f"Claim ID: {claim['claim_id']} | Patient: {claim['patient_name']} | Amount: ${claim['amount']:.2f} | Status: {claim['status']}")

    total_amount += claim["amount"]

    if claim["status"] == "Denied":
        print("  *** CLAIM DENIED ***")
        denied_count += 1
    elif claim["amount"] > 3000:
        print("  >> HIGH VALUE CLAIM")
        high_value_count += 1
    else:
        print("  STANDARD CLAIM")

print()
print("--- SUMMARY ---")
print(f"Total claims processed : {len(claims)}")
print(f"Total dollar amount    : ${total_amount:.2f}")
print(f"Denied claims          : {denied_count}")
print(f"High value claims      : {high_value_count}")
