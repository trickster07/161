FROM alpine:latest

RUN apk add --update python3 py3-pip git tcpdump

RUN git clone https://github.com/trickster07/16 1
WORKDIR 1
# COPY requirements.txt .
# COPY api.txt .
# COPY bots.txt .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "1.py"]
