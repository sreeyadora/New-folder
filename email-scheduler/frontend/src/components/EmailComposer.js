import React, { useState } from "react";

export default function ComposeEmailModal({ onClose }) {
  const [to, setTo] = useState("");
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");

  return (
    <div style={overlayStyle}>
      <div style={modalStyle}>
        <h3>Compose Email</h3>

        <input
          placeholder="Recipient email"
          value={to}
          onChange={(e) => setTo(e.target.value)}
          style={inputStyle}
        />

        <input
          placeholder="Subject"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          style={inputStyle}
        />

        <textarea
          placeholder="Email body"
          value={body}
          onChange={(e) => setBody(e.target.value)}
          style={inputStyle}
        />

        <div style={{ marginTop: 10 }}>
          <button onClick={onClose}>Cancel</button>
          <button style={{ marginLeft: 10 }}>Schedule</button>
        </div>
      </div>
    </div>
  );
}

const overlayStyle = {
  position: "fixed",
  top: 0,
  left: 0,
  width: "100vw",
  height: "100vh",
  background: "rgba(0,0,0,0.3)",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

const modalStyle = {
  background: "#fff",
  padding: 20,
  width: 400,
  borderRadius: 8,
};

const inputStyle = {
  width: "100%",
  marginBottom: 10,
  padding: 8,
};
