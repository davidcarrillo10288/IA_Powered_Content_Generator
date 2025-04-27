#### Project carried out for the Artificial Intelligence course at https://bootcampxperience.com/

#
# AI-Powered Content Generation Tool

## Overview

This project is a versatile AI-powered tool designed to generate and refine content for various platforms, including Instagram, TikTok, and more. It is highly customizable, allowing users to tailor the content to different target audiences, tones, and languages. The tool leverages advanced Large Language Models (LLMs) to create engaging and dynamic content based on product information scraped from e-commerce websites.

# Folder Structure

```
project-root/
│
├── backend/
│   ├── Dockerfile               # Docker configuration for the backend
│   ├── models/                  # Pydantic model files
│   ├── prompts/                 # Prompt template files
│   ├── src/                     # Backend source code
│   │   ├── content_generator.py  # Content generation logic
│   │   ├── image_describer.py    # Image description handling
│   │   ├── llm.py                # LLM interaction module
│   │   ├── scraping.py           # Web scraping functionality
│   │   └── server.py             # FastAPI server
│   └── requirements.txt          # Python dependencies for the backend
│
├── frontend/
│   ├── Dockerfile               # Docker configuration for the frontend
│   ├── models/                  # Pydantic model files
│   ├── src/                     # Frontend source code
│   │   ├── generate_content.py   # Content generation logic for UI
│   │   └── ui.py                 # User interface logic
│   └── requirements.txt          # Python dependencies for the frontend
│
├── README.md                    # Project documentation
└── docker-compose.yml            # Docker Compose configuration
```

## Features

- **Content Generation**: Automatically generates content based on product details such as title, price, description, and available sizes.
- **Tone Refinement**: Adjusts the tone and language of the content to match a new target audience and tone specified by the user.
- **Image Description**: Describes product images to provide additional context for the content.
- **Web Scraping**: Extracts product information from e-commerce websites like Falabella.
- **API Integration**: Provides a FastAPI backend for content generation and a Streamlit frontend for user interaction.

## Project Structure

The project is divided into two main components:

1. **Backend**: Handles the logic for content generation, tone refinement, and web scraping. It is built using FastAPI and runs on port **8004**.
2. **Frontend**: Provides a user-friendly interface for inputting product URLs and generating content. It is built using Streamlit and runs on port **8501**.

### Backend Structure

- **Dockerfile**: Defines the environment for the backend service.
- **models/**: Contains Pydantic models for data validation.
- **prompts/**: Stores templates for generating and refining content.
- **src/**: Contains the main logic for content generation, image description, and web scraping.
  - **content_generator.py**: Generates and refines content using LLMs.
  - **image_describer.py**: Describes product images.
  - **llm.py**: Handles interactions with the Groq API.
  - **scraping.py**: Scrapes product information from e-commerce websites.
  - **server.py**: Defines the FastAPI endpoints for content generation.

### Frontend Structure

- **Dockerfile**: Defines the environment for the frontend service.
- **models/**: Contains Pydantic models for data validation.
- **src/**: Contains the Streamlit UI and logic for interacting with the backend.
  - **generate_content.py**: Sends requests to the backend to generate content.
  - **ui.py**: Defines the Streamlit interface for user interaction.

## Documentation of Files

### Backend

- **Dockerfile**: Configures the Docker environment for the backend service.
- **models/content_generation_models.py**: Defines Pydantic models for content generation and tone refinement.
- **prompts/content_generation_prompts.py**: Contains templates for generating content.
- **prompts/tone_generator.py**: Contains templates for refining content tone.
- **src/content_generator.py**: Handles the generation and refinement of content using LLMs.
- **src/image_describer.py**: Describes product images using the Groq API.
- **src/llm.py**: Manages interactions with the Groq API.
- **src/scraping.py**: Scrapes product information from e-commerce websites.
- **src/server.py**: Defines FastAPI endpoints for content generation.

### Frontend

- **Dockerfile**: Configures the Docker environment for the frontend service.
- **models/content_generation_models.py**: Defines Pydantic models for content generation.
- **src/generate_content.py**: Sends requests to the backend to generate content.
- **src/ui.py**: Provides the Streamlit interface for user interaction.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.
- A `.env` file with the necessary environment variables (e.g., `GROQ_API_KEY`, `BACKEND_URL`).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai-content-generation-tool.git
   cd ai-content-generation-tool
   ```

2. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Access the frontend in your browser at `http://localhost:8501`.

### Usage

1. **Input Product URL**: Enter the URL of the product you want to generate content for.
2. **Set Target Audience**: Specify the new target audience for the content.
3. **Choose Tone**: Select the tone you want the content to have (e.g., funny, serious, trendy).
4. **Select Language**: Choose the language for the content (e.g., Spanish, English).
5. **Generate Content**: Click the "Generar Guion" button to generate the content.
6. **Download Content**: Once generated, you can download the content in JSON format.

## API Endpoints

### Backend
- **Swagger Docs**: Accessible at `http://localhost:8004/docs`
  - Provides a user interface to interact with the API using Swagger Docs.

- **Health Check**: `GET /health`
  - Checks the health of the API.
  
- **Content Generation**: `POST /content_generator`
  - Generates content based on the provided product URL, target audience, tone, and language.

### Frontend

- **Streamlit UI**: Accessible at `http://localhost:8501`
  - Provides a user interface for generating and downloading content.

