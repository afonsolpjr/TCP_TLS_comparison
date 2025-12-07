FROM python:slim

WORKDIR /opt

COPY TCPclient.py TCPclient.py
COPY server.crt server.crt

ENTRYPOINT ["python3", "/opt/TCPclient.py"]