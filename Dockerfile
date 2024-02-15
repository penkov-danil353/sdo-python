FROM alpine:edge as build
LABEL authors="sidecuter"
WORKDIR /var/build

COPY cpp_libs/parser .
RUN apk add g++ \
    && g++ -c -o library.o library.cpp -fPIC && g++ -shared -o libparse.so library.o

FROM alpine:edge
WORKDIR /var/server

RUN apk add --no-cache python3 py3-pip python3-dev build-base libffi-dev
RUN python3 -m venv venv
ENV PATH="/var/server/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY --from=build /var/build/libparse.so /usr/lib
COPY . .
