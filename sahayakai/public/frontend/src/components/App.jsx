import React from 'react';
import Header from './header';
import Footer from './footer';
// import Chatbot from './Chatbot';
import MessageDisplay from './messagedisplay';
import MessageInput from './messageinput';
const App = () => (
  <div className="app">
    <Header />
    <MessageDisplay />

    <MessageInput />
    <Footer />
  </div>
);

export default App;
