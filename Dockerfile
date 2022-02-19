FROM tiangolo/uwsgi-nginx-flask:python3.8

ENV NGINX_MAX_UPLOAD 1m

RUN apt-get update -y && apt-get install -y npm
# Upgrade to the latest version of Node.js
RUN npm install n -g && n latest && hash -r && npm install -g npm@8.3.2 

RUN mkdir /var/log/konfu && chown nginx:nginx /var/log/konfu

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./root_bash_history /root/.bash_history
COPY ./root_vimrc /root/.vimrc

COPY supervisord/*.conf /etc/supervisor/conf.d
#RUN rm /etc/supervisor/supervisord.conf
RUN chown -R nginx:nginx /app
RUN npm install -g yarn
#USER appuser
COPY ./app/package.json ./app/requirements.txt /app 
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY ./app /app
WORKDIR /app
RUN yarn install
USER root
