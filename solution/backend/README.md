# Solution

## Introduction
This project is designed to showcase a full-stack solution incorporating a FastAPI backend, a Streamlit frontend, and MLflow for model tracking and experiment management (not integrated in this assignment). It demonstrates a practical implementation of a machine learning pipeline, from data preprocessing and model training to prediction serving and result visualization.

## Quickstart
Before starting, ensure Docker is installed on your system. This project uses Docker Compose for easy orchestration of multiple services.

### Running the Application
To get the application up and running, execute the following command in the root directory of the project:
```bash
docker-compose up --build
```

You can also run locally 

for frontend go to frontend directory and use  
```bash
streamlit run main.py 
```

for backend go to backend directory and use 
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 
```
You can also refer Makefile for extra commands

### Project Structure

The project is organized into several key directories, each serving a specific function:
```bash

solution/
│
├── docker-compose.yml       # Docker Compose file to orchestrate containers
├── README.md                # Overview and setup instructions
│
├── backend/                 # Backend service with FastAPI
│   ├── config.yaml          # Configuration settings for the backend
│   ├── main.py              # Backend application entry point
│   ├── requirements.txt     # Python dependencies for the backend
│   ├── data/                # Directory for input data
│   ├── results/             # Directory for storing output results
│   ├── src/                 # Backend source code
│   │   ├── application/     # Application logic, e.g., workflows
│   │   ├── domain/          # Core logic for data processing and model training
│   │   └── infrastructure/  # Infrastructure code, e.g., data loading, health checks
│   └── tests/               # Backend test cases
│
├── data/                    # General data storage (optional)
│
├── frontend/                # Frontend service with Streamlit
│   ├── main.py              # Frontend application entry point
│   ├── requirements.txt     # Python dependencies for the frontend
│   └── src/                 # Frontend source code
│       ├── application/     # Frontend application logic
│       ├── domain/          # Domain-specific frontend logic
│       └── infrastructure/  # Infrastructure for frontend, e.g., backend communication
│
└── mlflow/                  # Not Implemented; we can use pre-built docker image 

```