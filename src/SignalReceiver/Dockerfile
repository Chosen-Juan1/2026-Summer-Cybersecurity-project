FROM python:3

WORKDIR /app
RUN apt-get update && apt-get install -y libpcap-dev tcpdump
COPY requirements.txt .
RUN pip install -r requirements.txt

# do last to avoid rebuilding the image every time we change the code
COPY src/SignalReceiver/ .
COPY .env .
EXPOSE 5000

CMD ["python", "Receiver.py"]