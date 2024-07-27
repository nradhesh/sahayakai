import React, { useState } from 'react';

const MessageInput = ({ onSend }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    onSend(input);
    setInput('');
  };

  return (
    <div className="message-input">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message here..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default MessageInput;
