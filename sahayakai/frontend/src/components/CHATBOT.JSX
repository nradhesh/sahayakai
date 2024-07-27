import React from 'react';
import MessageInput from './messageinput';
import MessageDisplay from './messagedisplay';

const Chatbot = () => {
  return (
    <div className="chatbot">
      <MessageDisplay />
      <MessageInput />
    </div>
  );
};
export default Chatbot;