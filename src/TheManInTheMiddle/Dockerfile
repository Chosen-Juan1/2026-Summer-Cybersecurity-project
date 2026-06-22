FROM python:3

WORKDIR /app
COPY src/TheManInTheMiddle/ .

RUN apt-get update && apt-get install -y libpcap-dev tcpdump
COPY requirements.txt .
COPY src/Attacks .
RUN pip install -r requirements.txt

# CMD ["ls"]
CMD ["python", "Man.py"]