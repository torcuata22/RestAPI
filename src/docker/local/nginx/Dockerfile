FROM nginx:1.23.3-alpine 

RUN rm /etc/nginx/conf.d/default.conf 

RUN mkdir -p /home/app/staticfiles
RUN chmod -R 755 /home/app/staticfiles

COPY ./default.conf /etc/nginx/conf.d/default.conf