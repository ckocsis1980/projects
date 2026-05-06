// Week 13 – React Claims Card Component
// To run this file, you need a React environment. The easiest way:
//   1. Run: npx create-react-app bluestar-claims
//   2. Replace src/App.js contents with this file's code, or
//   3. Use an online sandbox like codesandbox.io or stackblitz.com

import React from "react";

// ─────────────────────────────────────────────────────────────────────────────
// WHAT IS A REACT COMPONENT?
//
// A component is a reusable building block for your UI — think of it like a
// custom HTML tag that you define yourself. It is a JavaScript function that
// returns JSX (HTML-like syntax). Once defined, you can use it as many times
// as you want just by writing <ComponentName />.
//
// Example: <ClaimCard /> below is a component we define, then reuse for every
// claim in our list.
// ─────────────────────────────────────────────────────────────────────────────

// ─────────────────────────────────────────────────────────────────────────────
// WHAT ARE PROPS?
//
// "Props" (short for properties) are how you pass data INTO a component from
// the outside — similar to how HTML attributes pass values into tags.
//
// Example: <ClaimCard claimId="CLM-001" patientName="Alice Hart" />
//   → inside ClaimCard, props.claimId === "CLM-001"
//   → inside ClaimCard, props.patientName === "Alice Hart"
//
// Props flow ONE WAY: parent → child. The child reads them but never changes
// them directly. This makes data flow predictable and easy to trace.
// ─────────────────────────────────────────────────────────────────────────────

// Sample claims data – an array of plain objects.
// In a real app this would come from an API call.
const SAMPLE_CLAIMS = [
  {
    claimId: "CLM-2024-001",
    patientName: "Alice Hart",
    amount: 1250.0,
    status: "Approved",
    patientResponsibility: 150.0,
  },
  {
    claimId: "CLM-2024-002",
    patientName: "Robert Nguyen",
    amount: 3780.5,
    status: "Pending",
    patientResponsibility: 500.0,
  },
  {
    claimId: "CLM-2024-003",
    patientName: "Sandra Okafor",
    amount: 620.75,
    status: "Denied",
    patientResponsibility: 620.75,
  },
  {
    claimId: "CLM-2024-004",
    patientName: "James Whitfield",
    amount: 2100.0,
    status: "Approved",
    patientResponsibility: 210.0,
  },
];

// ─────────────────────────────────────────────────────────────────────────────
// ClaimCard Component
//
// Receives one claim's data via props and renders a styled card for it.
// Props expected:
//   claimId            (string)  – unique claim identifier
//   patientName        (string)  – full name of the patient
//   amount             (number)  – total billed amount in dollars
//   status             (string)  – "Approved" | "Pending" | "Denied"
//   patientResponsibility (number) – amount the patient owes
// ─────────────────────────────────────────────────────────────────────────────
function ClaimCard({ claimId, patientName, amount, status, patientResponsibility }) {
  // Pick a badge color based on the claim status so it stands out at a glance.
  const statusColors = {
    Approved: { background: "#e8f5e9", color: "#2e7d32", border: "#a5d6a7" },
    Pending:  { background: "#fff8e1", color: "#f57f17", border: "#ffe082" },
    Denied:   { background: "#ffebee", color: "#c62828", border: "#ef9a9a" },
  };

  const badge = statusColors[status] ?? statusColors.Pending;

  // Inline styles keep this file self-contained (no separate CSS file needed).
  // In a larger project you'd use a CSS module or a library like Tailwind.
  const styles = {
    card: {
      backgroundColor: "#ffffff",
      border: "1px solid #bbdefb",
      borderRadius: "10px",
      padding: "24px",
      width: "320px",
      boxShadow: "0 2px 8px rgba(13, 71, 161, 0.12)",
      fontFamily: "'Segoe UI', Arial, sans-serif",
      color: "#1a2b3c",
    },
    header: {
      backgroundColor: "#0d47a1",
      color: "#ffffff",
      margin: "-24px -24px 16px -24px",
      padding: "14px 24px",
      borderRadius: "10px 10px 0 0",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
    },
    claimId: {
      fontSize: "13px",
      fontWeight: "600",
      letterSpacing: "0.5px",
    },
    patientName: {
      fontSize: "18px",
      fontWeight: "700",
      marginBottom: "14px",
      color: "#0d47a1",
    },
    row: {
      display: "flex",
      justifyContent: "space-between",
      marginBottom: "8px",
      fontSize: "14px",
    },
    label: {
      color: "#546e7a",
      fontWeight: "500",
    },
    value: {
      fontWeight: "600",
      color: "#1a2b3c",
    },
    badge: {
      display: "inline-block",
      padding: "3px 10px",
      borderRadius: "12px",
      fontSize: "12px",
      fontWeight: "700",
      backgroundColor: badge.background,
      color: badge.color,
      border: `1px solid ${badge.border}`,
    },
    divider: {
      borderTop: "1px solid #e3f0fc",
      margin: "12px 0",
    },
    responsibility: {
      display: "flex",
      justifyContent: "space-between",
      backgroundColor: "#eaf2fb",
      borderRadius: "6px",
      padding: "10px 12px",
      marginTop: "12px",
    },
    responsibilityLabel: {
      fontSize: "13px",
      color: "#0d47a1",
      fontWeight: "600",
    },
    responsibilityValue: {
      fontSize: "15px",
      color: "#0d47a1",
      fontWeight: "700",
    },
  };

  // Helper: format a number as USD currency string
  const usd = (n) =>
    n.toLocaleString("en-US", { style: "currency", currency: "USD" });

  // JSX returned by the component — this is what gets rendered to the DOM.
  // Notice how we use the props variables (claimId, patientName, etc.) to
  // fill in the dynamic parts of the card.
  return (
    <div style={styles.card}>
      {/* Card header: dark-blue bar with the claim ID */}
      <div style={styles.header}>
        <span style={styles.claimId}>{claimId}</span>
        <span style={styles.badge}>{status}</span>
      </div>

      {/* Patient name */}
      <div style={styles.patientName}>{patientName}</div>

      {/* Billed amount */}
      <div style={styles.row}>
        <span style={styles.label}>Total Billed</span>
        <span style={styles.value}>{usd(amount)}</span>
      </div>

      <div style={styles.divider} />

      {/* Patient responsibility highlight */}
      <div style={styles.responsibility}>
        <span style={styles.responsibilityLabel}>Patient Responsibility</span>
        <span style={styles.responsibilityValue}>{usd(patientResponsibility)}</span>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// App Component (root component)
//
// This is the top-level component that React renders first. It owns the data
// (SAMPLE_CLAIMS) and maps each claim object to a <ClaimCard />, passing the
// fields as props. This is the standard React pattern: parent holds data,
// children display it.
// ─────────────────────────────────────────────────────────────────────────────
function App() {
  const styles = {
    page: {
      minHeight: "100vh",
      backgroundColor: "#eaf2fb",
      fontFamily: "'Segoe UI', Arial, sans-serif",
    },
    header: {
      backgroundColor: "#0d47a1",
      color: "#ffffff",
      padding: "20px 40px",
      display: "flex",
      alignItems: "center",
      gap: "16px",
    },
    logo: {
      fontSize: "22px",
      fontWeight: "700",
      letterSpacing: "1px",
    },
    subtitle: {
      fontSize: "13px",
      opacity: 0.8,
    },
    main: {
      padding: "40px",
    },
    heading: {
      fontSize: "22px",
      fontWeight: "700",
      color: "#0d47a1",
      marginBottom: "8px",
    },
    subheading: {
      fontSize: "14px",
      color: "#546e7a",
      marginBottom: "32px",
    },
    // CSS Grid spreads the cards into a responsive multi-column layout.
    grid: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))",
      gap: "24px",
    },
  };

  return (
    <div style={styles.page}>
      {/* Site header */}
      <header style={styles.header}>
        <div>
          <div style={styles.logo}>BlueStar Health Plan</div>
          <div style={styles.subtitle}>Member Claims Portal</div>
        </div>
      </header>

      <main style={styles.main}>
        <div style={styles.heading}>Recent Claims</div>
        <div style={styles.subheading}>
          {SAMPLE_CLAIMS.length} claims found
        </div>

        {/*
          Map over the claims array and render one <ClaimCard /> per item.
          The "key" prop is required by React whenever you render a list —
          it helps React efficiently track which items changed, were added,
          or were removed. Always use a stable unique value (like an ID).
        */}
        <div style={styles.grid}>
          {SAMPLE_CLAIMS.map((claim) => (
            <ClaimCard
              key={claim.claimId}
              claimId={claim.claimId}
              patientName={claim.patientName}
              amount={claim.amount}
              status={claim.status}
              patientResponsibility={claim.patientResponsibility}
            />
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
