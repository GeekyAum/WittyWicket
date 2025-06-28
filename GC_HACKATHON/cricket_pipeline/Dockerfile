# Use the official Pathway base image
FROM pathwaycom/pathway:latest

# Set the working directory
WORKDIR /app/cricket_pipeline

# Copy the requirements file
COPY ./cricket_pipeline/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install git and clone the cricket-api repository
RUN apt-get update && \
    apt-get install -y git 

# Install Tesseract OCR
RUN apt-get install -y tesseract-ocr tesseract-ocr-eng

# Add this before the CMD line
RUN pip install Flask-Cors

# Set the TESSDATA_PREFIX environment variable 
ENV TESSDATA_PREFIX=/usr/share/tesseract/tessdata

# Copy the entire project
COPY ./cricket_pipeline .

# Add cricket_pipeline to PYTHONPATH
ENV PYTHONPATH="/app"


# Expose port
EXPOSE 9000

# Start command - run your Python script directly
CMD ["python", "main.py"]
