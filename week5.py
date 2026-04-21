# week5.py - Variables in Python using healthcare claims data examples

# String variable: stores the patient's full name
patient_name = "Jane Doe"

# Integer variable: stores a unique claim ID number
claim_id = 100432

# Float variable: stores the dollar amount billed for the claim
claim_amount = 1875.50

# String variable: stores the current processing status of the claim
claim_status = "Approved"

# String variable: stores the patient's insurance member ID
member_id = "XYZ-00291847"

# Float variable: stores the amount the insurance plan paid
insurance_paid = 1500.00

# Float variable: stores the remaining amount owed by the patient
patient_responsibility = claim_amount - insurance_paid

# Boolean variable: indicates whether the claim has been fully processed
is_processed = True

# String variable: stores the date the claim was submitted
submission_date = "2026-04-15"

# Integer variable: stores the patient's age
patient_age = 42

# Print a summary to verify the variables
print("Claim Summary")
print("Patient:", patient_name)
print("Claim ID:", claim_id)
print("Claim Amount: $", claim_amount)
print("Status:", claim_status)
print("Patient Owes: $", patient_responsibility)

# Check if the patient balance requires follow-up
if patient_responsibility > 300:
    print("FOLLOW UP REQUIRED")
else:
    print("BALANCE ACCEPTABLE")

# Check if the claim was denied and a denial notice needs to be sent
if claim_status == "Denied":
    print("DENIAL NOTICE REQUIRED")
else:
    print("NO ACTION NEEDED")
