
# Calgary-Hacks-2026 AI Project

## Overview
This project is an AI-powered music search and recommendation system developed for Calgary Hacks 2026. It leverages deep learning models to analyze and retrieve music tracks based on user queries.

## Features
- Music search using audio features
- Song recommendation system
- Deep learning model integration (CNN14)
- REST API for music retrieval
- Dockerized for easy deployment

## Project Structure
- `main.py`: Entry point for running the application
- `model.py`: Implements image functionality
- `music.py`: Handles music data processing
- `search.py`: Implements search functionality
- `songret.py`: Song retrieval and recommendation logic
- `requirements.txt`: Python dependencies
- `Dockerfile` & `docker-compose.yml`: Containerization setup
- `Cnn14_DecisionLevelMax_mAP=0.385.pth`: Pre-trained model weights

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
3. **Run the application:**
	```bash
	python main.py
	```
4. **(Optional) Run with Docker:**
	```bash
	docker-compose up --build
	```

## Usage
- Access the API endpoints as described in the code or documentation.
- Use the search and recommendation features to find music tracks.

## Requirements
- Python 3.8+
- See `requirements.txt` for Python packages
- Docker (optional, for containerized deployment)

## Authors
- Sreerag 
- Nik
- Mohammad 
- Aarav 
- Keegan
