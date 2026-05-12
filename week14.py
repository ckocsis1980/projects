import sqlite3
from datetime import date

# Connect to the SQLite database file. If claims.db does not exist,
# sqlite3 will create it in the current working directory.
connection = sqlite3.connect("claims.db")
cursor = connection.cursor()

# Drop the CLAIMS table if it already exists so the script can be re-run
# without raising an "already exists" error or duplicating rows.
cursor.execute("DROP TABLE IF EXISTS CLAIMS")

# Create the CLAIMS table. claim_id is the primary key so each claim is
# uniquely identifiable. Monetary columns use REAL to store dollar amounts.
cursor.execute("""
    CREATE TABLE CLAIMS (
        claim_id INTEGER PRIMARY KEY,
        patient_name TEXT NOT NULL,
        date_of_service TEXT NOT NULL,
        provider TEXT NOT NULL,
        amount REAL NOT NULL,
        insurance_paid REAL NOT NULL,
        patient_responsibility REAL NOT NULL,
        status TEXT NOT NULL
    )
""")

# Sample claims data. Each tuple matches the column order of the CLAIMS
# table so it can be passed straight into executemany().
sample_claims = [
    (1001, "John Smith",      "2026-01-15", "Dr. Adams",      450.00, 360.00,  90.00, "Paid"),
    (1002, "Mary Johnson",    "2026-02-03", "Dr. Patel",     1200.50, 960.40, 240.10, "Paid"),
    (1003, "Robert Lee",      "2026-02-21", "Dr. Garcia",     275.75, 220.60,  55.15, "Pending"),
    (1004, "Linda Martinez",  "2026-03-10", "Dr. Adams",     3050.00,   0.00,   0.00, "Denied"),
    (1005, "James Anderson",  "2026-04-05", "Dr. Thompson",   825.00, 660.00, 165.00, "Paid"),
]

# Use parameterized INSERT with executemany() to add all five records in
# one call. The ? placeholders prevent SQL injection and let sqlite3
# handle the value escaping for us.
cursor.executemany("""
    INSERT INTO CLAIMS (
        claim_id, patient_name, date_of_service, provider,
        amount, insurance_paid, patient_responsibility, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", sample_claims)

# Commit the transaction so the inserted rows are saved to claims.db.
connection.commit()

# SELECT every column and row from CLAIMS, ordered by claim_id so the
# report comes out in a predictable order regardless of insert order.
cursor.execute("SELECT claim_id, patient_name, date_of_service, provider, "
               "amount, insurance_paid, patient_responsibility, status "
               "FROM CLAIMS ORDER BY claim_id")
rows = cursor.fetchall()

# Print a formatted report. The column widths are tuned to fit the
# sample data; f-string format specs handle alignment and dollar
# formatting for the monetary columns.
print("=" * 110)
print(f"{'CLAIMS REPORT':^110}")
print(f"Generated: {date.today().isoformat():^99}")
print("=" * 110)
print(f"{'ID':<6}{'Patient':<18}{'Date':<12}{'Provider':<15}"
      f"{'Amount':>12}{'Ins Paid':>12}{'Pt Resp':>12}{'Status':>12}")
print("-" * 110)

total_amount = 0.0
total_insurance = 0.0
total_patient = 0.0

for row in rows:
    claim_id, name, dos, provider, amount, ins_paid, pt_resp, status = row
    print(f"{claim_id:<6}{name:<18}{dos:<12}{provider:<15}"
          f"${amount:>10,.2f}${ins_paid:>10,.2f}${pt_resp:>10,.2f}{status:>12}")
    total_amount += amount
    total_insurance += ins_paid
    total_patient += pt_resp

print("-" * 110)
print(f"{'TOTALS':<51}${total_amount:>10,.2f}${total_insurance:>10,.2f}"
      f"${total_patient:>10,.2f}")
print("=" * 110)
print(f"Records returned: {len(rows)}")

# Second query: use a WHERE clause to filter for claims whose status is
# "Denied". The parameter is passed as a tuple so sqlite3 binds it
# safely instead of interpolating the value into the SQL string.
cursor.execute("SELECT claim_id, patient_name, date_of_service, provider, amount "
               "FROM CLAIMS WHERE status = ? ORDER BY claim_id", ("Denied",))
denied_rows = cursor.fetchall()

print()
print("=" * 110)
print(f"{'DENIED CLAIMS':^110}")
print("=" * 110)
print(f"{'ID':<6}{'Patient':<18}{'Date':<12}{'Provider':<15}{'Amount':>12}")
print("-" * 110)

denied_total = 0.0
for claim_id, name, dos, provider, amount in denied_rows:
    print(f"{claim_id:<6}{name:<18}{dos:<12}{provider:<15}${amount:>11,.2f}")
    denied_total += amount

print("-" * 110)
print(f"Denied claim count: {len(denied_rows)}")
print(f"Total denied amount: ${denied_total:,.2f}")
print("=" * 110)

# Close the connection to release the database file handle.
connection.close()
