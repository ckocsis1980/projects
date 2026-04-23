def evaluate_claim(claim):
    # Check if the claim was denied regardless of amount
    if claim.get("status") == "Denied":
        return "DENIED"

    # Flag claims above 3000 as high value for extra review
    if claim.get("amount", 0) > 3000:
        return "HIGH VALUE"

    # Default case: claim is within normal processing range
    return "STANDARD CLAIM"


test_claims = [
    {"id": "C001", "amount": 1200, "status": "Approved"},
    {"id": "C002", "amount": 4500, "status": "Approved"},
    {"id": "C003", "amount": 800,  "status": "Denied"},
    {"id": "C004", "amount": 3001, "status": "Approved"},
    {"id": "C005", "amount": 250,  "status": "Pending"},
]

for claim in test_claims:
    result = evaluate_claim(claim)
    print(f"Claim {claim['id']}: {result}")


def calculate_patient_responsibility(claim):
    # Extract the three billing components from the claim
    amount = claim["amount"]
    insurance_paid = claim["insurance_paid"]
    deductible = claim["deductible"]

    # Patient always owes the deductible upfront before insurance applies
    # Insurance then covers insurance_paid of the remaining balance
    remaining_after_deductible = amount - deductible

    # Any balance left after insurance pays is also the patient's responsibility
    # max() prevents a negative value if insurance overpays the remainder
    patient_owes = deductible + max(0, remaining_after_deductible - insurance_paid)

    return patient_owes


patient_claims = [
    {"id": "P001", "amount": 5000, "insurance_paid": 3000, "deductible": 500},
    {"id": "P002", "amount": 1200, "insurance_paid": 1200, "deductible": 300},
    {"id": "P003", "amount": 800,  "insurance_paid": 200,  "deductible": 150},
]

print()
for claim in patient_claims:
    owed = calculate_patient_responsibility(claim)
    print(f"Claim {claim['id']}: Patient owes ${owed:.2f}")
