FROM node:23-alpine

WORKDIR /code/genai_client

COPY app/package*.json ./

RUN npm install

COPY app/ .

CMD ["npm", "run", "dev"]
