FROM python:3

WORKDIR /app
RUN apt-get update && apt-get install -y libpcap-dev tcpdump
COPY requirements.txt .
COPY src/Attacks .
COPY src/Database .
RUN pip install -r requirements.txt

# do last to avoid rebuilding the image every time we change the code
COPY --exclude=SignalReceiver --exclude=SignalSender --exclude=TheManinTheMiddle src .
COPY .env .

# CMD ["ls"]
CMD ["python", "-m", "Server.server"]