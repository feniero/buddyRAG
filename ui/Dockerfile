FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app-ui.py .

EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app-ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
