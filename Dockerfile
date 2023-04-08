FROM debian:11.6
LABEL authors="sidecuter"

WORKDIR /var/server

COPY . .

RUN apt-get -y update && apt-get -y upgrade \
    && apt-get -y install python3 python3-pip
RUN python3 -m pip install -r requirements.txt

#CMD ["python3 -m uvicorn main:app --reload"]