import React, { useState } from "react";
import ComposeEmailModal from "../components/EmailComposer";
import ScheduledEmailsTable from "../components/PendingEmailsTable";
import SentEmailsTable from "../components/DeliveryHistoryTable";

export default function UserDashboard({ user }) {
  const [showModal, setShowModal] = useState(false);

  return (
    <div style={{ padding: 20 }}>
      <h1>Dashboard</h1>

      <h2>Hello, {user?.name} 👋</h2>
      <p>Email: {user?.email}</p>

      <button onClick={() => setShowModal(true)}>
        Compose New Email
      </button>

      {showModal && (
        <ComposeEmailModal onClose={() => setShowModal(false)} />
      )}

      <hr style={{ margin: "20px 0" }} />

      <h3>Scheduled Emails</h3>
      <ScheduledEmailsTable />

      <h3>Sent Emails</h3>
      <SentEmailsTable />
    </div>
  );
}
