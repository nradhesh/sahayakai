import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import MessageInput from './MessageInput';
import MessageDisplay from './MessageDisplay';
import AboutUs from './AboutUs';
import { fetchRecommendations } from '../api';
import '../App.css';

const App = () => {
  const [messages, setMessages] = useState([]);

  const handleSend = async (message) => {
    setMessages([...messages, { text: message, from: 'user' }]);
    try {
      const data = await fetchRecommendations(message);
      const recs = data.recommendations; 
      setMessages((msgs) => [
        ...msgs,
        { text: 'Here are some recommendations for you:', from: 'bot' },
        ...recs.map((rec) => ({ text: rec.SchemeName, from: 'bot' }))
      ]);
    } catch (error) {
      console.error("Error handling send:", error);
    }
  };

  return (
    <Router>
      <div className="app">
        <Header />
        {/* <nav>
          <Link to="/">Home</Link>
          <Link to="/about-us">About Us</Link>
        </nav> */}
        <Routes>
          <Route path="/" element={
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
          } />
          <Route path="/about-us" element={<AboutUs />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
};

export default App;