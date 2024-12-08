# Project Setup Guide

This project consists of a **frontend** and a **backend**, which need to run in separate terminals.

---

## Backend Setup

### Steps to set up the backend:

1. Create a virtual environment:
   ```bash
   python -m venv venv
2. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
3. Upgrade pip:
   ```bash
   python -m pip install --upgrade pip
4. Install the required packages:
   ```bash
   python -m pip install flask flask_cors numpy pymongo scikit_learn torch torchvision torchaudio sentence_transformers
5. Run the Flask server:
   ```bash
   python -m flask --app .\app.py run


## Frontend Setup

### Steps to set up the Frontend:

1. Navigate to the frontend directory and install dependencies:
   ```bash
   npm install
2. Start the development server:
   ```bash
   npm run dev


