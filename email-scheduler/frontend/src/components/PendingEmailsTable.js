import React from "react";

export default function ScheduledEmailsTable() {
  const data = [
    { to: "test1@gmail.com", subject: "Interview", time: "10:30 AM" },
    { to: "test2@gmail.com", subject: "Follow up", time: "12:00 PM" },
  ];

  return (
    <table border="1" cellPadding="8" style={{ marginBottom: 20 }}>
      <thead>
        <tr>
          <th>To</th>
          <th>Subject</th>
          <th>Scheduled Time</th>
        </tr>
      </thead>
      <tbody>
        {data.map((email, i) => (
          <tr key={i}>
            <td>{email.to}</td>
            <td>{email.subject}</td>
            <td>{email.time}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
