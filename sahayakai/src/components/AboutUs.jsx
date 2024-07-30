// src/components/AboutUs.jsx
import React from 'react';
//import './AboutUs.css';

const AboutUs = () => (
  <div className="about-us-container">
    <div className="about-us-box">
      <section className="hero-section">
        <h2>About Sahayak AI</h2>
        <p>
          Sahayak AI is your trusted companion in navigating the complex landscape of government schemes. Our mission is to empower individuals with accurate and personalized information, making it easier to access and benefit from various programs.
        </p>
      </section>

      <section className="mission-section">
        <h3>Our Mission</h3>
        <p>
          We aim to simplify the process of discovering and understanding government schemes. By leveraging advanced AI technologies, we provide users with tailored recommendations that suit their unique needs and circumstances.
        </p>
      </section>

      <section className="team-section">
        <h3>Meet the Team</h3>
        <p>
          Our team consists of dedicated CSE (Computer Science and Engineering) students passionate about technology and its potential to drive positive change. We are committed to creating a user-friendly platform that serves the community effectively.
          <ol>
            <li>N Radhesh Shetty</li>
            <li>Nirmith MR</li>
            <li>Ifrah Naaz</li>
          </ol>
        </p>
      </section>

      <section className="goals-section">
        <h3>Our Goals</h3>
        <ul>
          <li>Provide accurate and up-to-date information on government schemes.</li>
          <li>Offer personalized recommendations based on user input.</li>
          <li>Enhance user experience through continuous improvement and innovation.</li>
        </ul>
      </section>
    </div>
  </div>
);

export default AboutUs;