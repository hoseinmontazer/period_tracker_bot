# Use official Python 3.12 image
FROM registry.uid.ir/uid/python:3.12.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements first (if you have requirements.txt)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# Copy the entire project
COPY . .

# Expose port if needed (Telegram bot does not need it)
# EXPOSE 8443

# Run the bot
CMD ["python", "bot.py"]
