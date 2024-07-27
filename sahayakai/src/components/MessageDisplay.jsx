import React from 'react';

const MessageDisplay = ({ messages }) => {
  return (
    <div className="message-display">
      {messages.map((msg, index) => (
        <div key={index} className={`message ${msg.from}`}>
          {msg.text}
        </div>
      ))}
    </div>
  );
};

export default MessageDisplay;
