FROM alpine:edge as build
WORKDIR /var/build

COPY cpp_libs/parser .

RUN apk add g++

RUN g++ -c -o library.o library.cpp -fPIC && g++ -shared -o libparse.so library.o

FROM alpine:edge
LABEL authors="sidecuter"

WORKDIR /var/server

COPY --from=build /var/build/libparse.so /usr/lib
COPY . .

RUN apk add python3 py3-pip\
    && python3 -m pip install -r requirements.txt
