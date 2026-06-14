FROM python:3

WORKDIR /app

COPY SignalSender/ .
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "Sender.py"]