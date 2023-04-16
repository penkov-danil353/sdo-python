FROM debian:11.6-slim as build
WORKDIR /var/build

COPY cpp_libs/parser .

RUN apt -y update && apt -y upgrade && apt -y install gcc g++

RUN g++ -c -o library.o library.cpp -fPIC && g++ -shared -o libparse.so library.o

FROM alpine:edge
LABEL authors="sidecuter"

WORKDIR /var/server

COPY --from=build /var/build/libparse.so /usr/lib
COPY . .

#RUN apt-get -y update && apt-get -y upgrade \
#    && apt-get -y install python3 python3-pip \
#    && python3 -m pip install -r requirements.txt
RUN apk add python3 py3-pip\
    && python3 -m pip install -r requirements.txt

#CMD ["python3", "parsewrapper.py"]



#CMD ["python3", "-m", "uvicorn", "main:app", "--reload"]
