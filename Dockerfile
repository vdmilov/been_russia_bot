FROM python:3.10

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app

COPY * ./

VOLUME been_bot_db

CMD [ "python", "main.py" ]