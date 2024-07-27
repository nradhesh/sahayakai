import React from 'react';
import MessageInput from './MessageInput';
import MessageDisplay from './MessageDisplay';

const Chatbot = () => {
  return (
    <div className="chatbot">
      <MessageDisplay />
      <MessageInput />
    </div>
  );
};

export default Chatbot;
