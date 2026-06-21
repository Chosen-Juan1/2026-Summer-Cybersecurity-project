FROM python:3

WORKDIR /app
COPY TheManInTheMiddle/ .

RUN apt-get update && apt-get install -y libpcap-dev tcpdump
COPY requirements.txt .
COPY Attacks .
RUN pip install -r requirements.txt

# CMD ["ls"]
CMD ["python", "Man.py"]