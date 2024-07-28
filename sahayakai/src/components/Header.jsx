// src/components/Header.jsx
import React from 'react';

const Header = () => (
  <header className="header">
    <div className="header-content">
      <h1>SAHAYAK AI</h1>
      <nav>
        <ul>
          <li><a href="/login">Login</a></li>
          <li><a href="/about-us">About Us</a></li>
        </ul>
      </nav>
    </div>
  </header>
);

export default Header;
