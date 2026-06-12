FROM node:22.12-alpine AS builder

WORKDIR /app

COPY web/package.json web/package-lock.json ./web/

WORKDIR /app/web

ARG VITE_BACK_URL
ENV VITE_BACK_URL=$VITE_BACK_URL

RUN npm install

COPY ./web .

RUN npm run build



FROM nginx:alpine AS runner

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*

COPY --from=builder /app/web/dist .

COPY ./web/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8200

CMD ["nginx", "-g", "daemon off;"]
