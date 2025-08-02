FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

RUN mkdir -p /var/www/certbot

CMD ["nginx", "-g", "daemon off;"]