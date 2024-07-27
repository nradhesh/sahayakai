import React, { useState } from 'react';
import Header from './Header';
import Footer from './Footer';
import MessageInput from './MessageInput';
import MessageDisplay from './MessageDisplay';
import { fetchRecommendations } from '../api';
// import './App.css';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  const handleSend = async (message) => {
    setMessages([...messages, { text: message, from: 'user' }]);
    const recs = await fetchRecommendations(message);
    setRecommendations(recs);
    setMessages((msgs) => [
      ...msgs,
      { text: 'Here are some recommendations for you:', from: 'bot' },
      ...recs.map((rec) => ({ text: rec[1], from: 'bot' })) 
    ]);
  };

  return (
    <div className="app">
      <Header />
      <div className="chatbot">
        <MessageDisplay messages={messages} />
        <MessageInput onSend={handleSend} />
      </div>
      <Footer />
    </div>
  );
};

export default App;
