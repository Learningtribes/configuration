# docker file for CI

FROM python:2
WORKDIR /app/
COPY requirements.txt pre-requirements.txt Makefile *.mk /app/
RUN make requirements
