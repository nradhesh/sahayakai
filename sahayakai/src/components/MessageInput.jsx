import React, { useState, useRef } from 'react';
import axios from 'axios';

const MessageInput = ({ onSend }) => {
  const [input, setInput] = useState('');
  const recognition = useRef(null);

  if (!recognition.current && 'webkitSpeechRecognition' in window) {
    recognition.current = new window.webkitSpeechRecognition();
    recognition.current.continuous = false;
    recognition.current.interimResults = false;
    recognition.current.lang = 'en-US'; // Default language

    recognition.current.onresult = async (event) => {
      const speechResult = event.results[0][0].transcript;
      const detectedLang = await detectLanguage(speechResult);
      const translatedText = await translateToEnglish(speechResult, detectedLang);
      setInput(translatedText);
    };

    recognition.current.onerror = (event) => {
      console.error("Speech recognition error", event.error);
    };
  }

  const detectLanguage = async (text) => {
    try {
      const response = await axios.post('https://libretranslate.de/detect', {
        q: text
      });
      return response.data[0].language;
    } catch (error) {
      console.error("Language detection error", error);
      return 'en'; // Default to English if detection fails
    }
  };

  const translateToEnglish = async (text, sourceLang) => {
    try {
      const response = await axios.post('https://libretranslate.de/translate', {
        q: text,
        source: sourceLang,
        target: 'en'
      });
      return response.data.translatedText;
    } catch (error) {
      console.error("Translation error", error);
      return text;
    }
  };

  const startRecognition = () => {
    if (recognition.current) {
      recognition.current.start();
    }
  };

  const handleSend = () => {
    if (input.trim() !== '') {
      onSend(input);
      setInput('');
    }
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
      <button onClick={startRecognition}>Voice</button>
    </div>
  );
};

export default MessageInput;
