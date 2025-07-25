FROM python:3.10-slim

WORKDIR /app

RUN mkdir input_files

#requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-u", "ingest-full.py"]
