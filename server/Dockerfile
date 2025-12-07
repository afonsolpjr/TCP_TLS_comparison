FROM python:slim

WORKDIR /opt

COPY TCPserver.py TCPserver.py
COPY server.crt server.crt
COPY server.key server.key

ENTRYPOINT ["python3", "/opt/TCPserver.py"]