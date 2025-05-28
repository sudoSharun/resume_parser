# RESUME PARSER

![Resume Parser Workflow](readme-assets/resume_parser_page.jpg)

## Table of Contents
- [Description](#description)
- [Tech Stack](#tech-stack)
- [Workflow](#workflow)
- [Setup](#setup)
- [Testing](#testing)

## Description
This project implements an intelligent and scalable resume parsing system designed to extract, classify, and structure information from resumes using Large Language Models (LLMs). Built with a microservices-based architecture and message queuing via RabbitMQ, the system ensures efficient asynchronous processing, making it suitable for high-volume resume analysis.

## Tech Stack
- Python
- RabbitMQ
- PostgreSQL
- AWS S3
- Docker

## Workflow

1. Accept resume and upload it to S3/SFTP, then push ID to RabbitMQ
2. RabbitMQ triggers downstream processing
3. Extract raw text from the resume based on file type
4. Split extracted text into chunks with overlap
5. Classify text chunks into predefined categories using an LLM
6. Parse each classified chunk into structured JSON using LLMs
7. Merge and clean all parsed data into a single JSON
8. Update the JSON into the PostgreSQL database and trigger a callback

## Setup

### Step 1: Clone the repository
```bash
git clone https://github.com/sudoSharun/resume_parser.git
cd resume_parser_lc
```

### Step 2: Set up `.env` variables
Create a `.env` file in the root directory and add the required environment variables. Refer to `.env.example` for guidance.

### Step 3: Install Docker
Ensure Docker is installed on your system. Follow the [official Docker installation guide](https://docs.docker.com/get-docker/) for your operating system.

### Step 4: Run Docker Compose
Start the application using Docker Compose:
```bash
docker-compose up --build
```
This will set up all necessary services, including the database and message broker.
