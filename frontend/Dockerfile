FROM node:23-alpine AS builder
WORKDIR /app

ADD package.json yarn.lock ./
RUN yarn install --immutable

ADD . ./
RUN yarn build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
