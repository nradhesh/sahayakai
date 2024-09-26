# Sahayak AI

Sahayak AI is a recommendation system built using React (with Vite) on the frontend and Flask with CORS on the backend. The system recommends government schemes to users based on their input keywords. It uses web scraping techniques to provide real-time information on schemes.

## Project Images
![WhatsApp Image 2024-09-26 at 17 14 19_469c11de](https://github.com/user-attachments/assets/cbb65921-738b-4fb4-8105-65c186d96f1e)
![WhatsApp Image 2024-09-26 at 17 18 43_9f147f85](https://github.com/user-attachments/assets/5c62751c-6c25-4ac7-80a1-0540b640f395)


## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [APIs](#apis)
- [License](#license)

## Features
- **RAG based application:** Uses vectorization and performs cosine similarity on the recieved prompt,
- **Reduced time:** Due to embedding already stored in .pkl file
- **Recommendation System:** Provides tailored scheme recommendations based on user input.
- **Web Scraping:** Fetches real-time scheme data using Selenium and BeautifulSoup.
- **Flask API and Flask CORS:** Handles backend operations and integrates with the recommendation engine.
- **React Frontend:** Built using Vite for fast and efficient development.

## Tech Stack

### Frontend
- **React** (with Vite)
### Backend
- **Flask**
- **Flask-CORS**
- **Pandas** (for data handling)
- **scikit-learn** (for TF-IDF and cosine similarity)
- **Selenium** (for web scraping)
- **BeautifulSoup** (for HTML parsing)

## Prerequisites

Ensure you have the following installed:

- **Node.js** (for React frontend)
- **Python 3.8+** (for Flask backend)
- **Google Chrome** (for Selenium web scraping)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/sahayak-ai.git
cd sahayak-ai
```

### 2. Setup the Backend

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. Install required Python dependencies:

   ```bash
   pip install requirements
   ```

4. Start the Flask server:

   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```

### 3. Setup the Frontend

1. Navigate to the frontend directory:

   ```bash
   cd ../frontend
   ```

2. Install Node.js dependencies:

   ```bash
   npm install
   ```

3. Start the Vite development server:

   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000` and the backend at `http://localhost:5000`.

## Usage

- Open the frontend and enter keywords in the input field.
- The Flask backend will process the request and provide scheme recommendations.
- The web scraper fetches real-time scheme information from the internet.

## APIs

### `/recommend` - POST

- **Description:** Accepts user keywords and returns a list of recommended schemes.
- **Request:**

  ```json
  {
    "keywords": "scholarship"
  }
  ```

- **Response:**

  ```json
  {
    "recommendations": [
      "Scheme 1 details",
      "Scheme 2 details",
      "Scheme 3 details"
    ]
  }
  ```

## License

This project is licensed under the MIT License.
```

This `README.md` includes the basic structure and usage instructions for both the frontend (React with Vite) and backend (Flask). Feel free to customize as per your requirements!
