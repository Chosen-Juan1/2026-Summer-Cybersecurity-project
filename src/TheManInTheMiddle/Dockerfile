FROM python:3

WORKDIR /app
RUN apt-get update && apt-get install -y libpcap-dev tcpdump
COPY requirements.txt .
COPY src/Attacks .
RUN pip install -r requirements.txt

# do last to avoid rebuilding the image every time we change the code
COPY --exclude=SignalReceiver --exclude=SignalSender src .
COPY .env .

EXPOSE 8501
# CMD ["python", "TheManInTheMiddle/TuesdayDemo_man.py"]
CMD ["streamlit", "run", "TheManInTheMiddle/TuesdayDemo_app.py"]