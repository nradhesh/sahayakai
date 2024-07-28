import React, { useState } from 'react';
import Header from './Header';
import Footer from './Footer';
import MessageInput from './MessageInput';
import MessageDisplay from './MessageDisplay';
import { fetchRecommendations } from '../api';
import '../App.css';

const App = () => {
  const [messages, setMessages] = useState([]);

  const handleSend = async (message) => {
    setMessages([...messages, { text: message, from: 'user' }]);
    const recs = await fetchRecommendations(message);
    console.log("Recommendations in App:", recs);  // Debug print
    setMessages((msgs) => [
      ...msgs,
      { text: 'Here are some recommendations for you:', from: 'bot' },
      ...recs.map((rec) => ({ text: rec[1], from: 'bot' })) // Assuming rec[1] is the scheme description
    ]);
  };
  return (
    <div className="app">
      <Header />
      <div className="chatbot">
        {messages.length === 0 ? (
          <div className="initial-display">
            <img src="/public/image.png" alt="Help Image" className="initial-image" />
            <p className="initial-text">Your help is just a few words of prompt</p>
          </div>
        ) : (
          <MessageDisplay messages={messages} />
        )}
        <MessageInput onSend={handleSend} />
      </div>
      <Footer />
    </div>
  );
};

export default App;
