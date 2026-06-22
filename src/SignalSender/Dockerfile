FROM python:3

WORKDIR /app

COPY src/SignalSender/ .
RUN apt-get update && apt-get install -y libpcap-dev tcpdump
COPY requirements.txt .
RUN pip install -r requirements.txt


EXPOSE 4000

CMD ["python", "Sender.py"]