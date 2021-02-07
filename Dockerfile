FROM python:latest

WORKDIR /app

COPY [ "src/", "." ]
COPY [ "requirements.txt", "." ]
COPY [ "token", "."]
COPY [ "binance-key", "." ]
COPY [ "binance-secret", "." ]

RUN pip install -r requirements.txt
RUN mkdir db

CMD [ "python", "main.py" ]
