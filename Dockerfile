FROM python:3.10-slim

ENV PORT 8000

WORKDIR /opt/app

RUN apt update && apt install git build-essential -y

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "run.sh"]