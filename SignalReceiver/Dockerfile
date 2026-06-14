FROM python:3

WORKDIR /app
COPY SignalReceiver/ .

RUN apt-get update && apt-get install -y libpcap-dev tcpdump
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "Receiver.py"]