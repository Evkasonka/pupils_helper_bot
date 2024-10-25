FROM python:3.9-slim

RUN apt update -y
RUN apt install -y python3
RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]