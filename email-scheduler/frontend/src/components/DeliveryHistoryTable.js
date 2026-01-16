import React from "react";

export default function SentEmailsTable() {
  const data = [
    { to: "client@gmail.com", subject: "Welcome", status: "Sent" },
    { to: "hr@gmail.com", subject: "Resume", status: "Sent" },
  ];

  return (
    <table border="1" cellPadding="8">
      <thead>
        <tr>
          <th>To</th>
          <th>Subject</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {data.map((email, i) => (
          <tr key={i}>
            <td>{email.to}</td>
            <td>{email.subject}</td>
            <td>{email.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
