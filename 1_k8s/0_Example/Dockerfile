FROM python:3.7

COPY requirements.txt /requirements.txt 
RUN pip install -r requirements.txt
RUN mkdir /app
COPY server.py /app/server.py
WORKDIR /app

EXPOSE 5000
CMD ["python", "/app/server.py"]