FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -p /var/www/certbot

RUN mkdir -p /etc/nginx/ssl && \
    openssl req -x509 -newkey rsa:2048 \
      -keyout /etc/nginx/ssl/fake-key.pem \
      -out /etc/nginx/ssl/fake-cert.pem \
      -days 365 \
      -nodes \
      -subj "/CN=fake"

RUN chmod 644 /etc/nginx/ssl/fake-cert.pem
RUN chmod 600 /etc/nginx/ssl/fake-key.pem

# Проверка (необязательно, но полезно для дебага)
RUN ls -la /etc/nginx/ssl

CMD ["nginx", "-g", "daemon off;"]