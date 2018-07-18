FROM python:2.7

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY run.py /app
COPY /exchange /app
COPY /tests /app
COPY /db /app

CMD python run.py
