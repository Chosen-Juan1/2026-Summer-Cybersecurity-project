FROM python:3

WORKDIR /app
RUN apt-get update && apt-get install -y libpcap-dev tcpdump
COPY requirements.txt .
COPY src/Attacks .
RUN pip install -r requirements.txt

# do last to avoid rebuilding the image every time we change the code
COPY src/TheManInTheMiddle/ .
COPY .env .

# CMD ["ls"]
CMD ["python", "Man.py"]