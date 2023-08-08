# build env
# FROM node:13.12.0-alpine as build
FROM node:14 as build
# FROM node:16 as build
WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . ./
RUN npm run build
CMD cp -r build result_build