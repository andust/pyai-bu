FROM golang:1.23-alpine

WORKDIR /code/user_srv

COPY ./app .

RUN go mod download

CMD [ "api" ]
