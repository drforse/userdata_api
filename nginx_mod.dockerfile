FROM nginx
EXPOSE 80
RUN rm /etc/nginx/conf.d/default.conf
COPY ./resources/nginx/conf.d /etc/nginx/conf.d
