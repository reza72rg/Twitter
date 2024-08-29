
FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app_twitter

COPY requirements.txt /app_twitter/
 

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN useradd -m myuser
USER myuser

COPY ./core /app_twitter

#CMD ["python3","manage.py","runserver","0.0.0.0:8000" ]