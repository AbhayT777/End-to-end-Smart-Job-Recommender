# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    libtesseract-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all files
COPY . .

# Download SpaCy model
RUN python -m spacy download en_core_web_sm

# Expose the Streamlit default port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

