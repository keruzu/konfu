#!/bin/bash

if compgen -G "/app/etc/nginx*.conf" > /dev/null ; then
  echo "Found custom Nginx configuration..."
  cp /app/etc/nginx*.conf /etc/nginx.conf.d
fi

if [[ -f /app/etc/custom-uwsgi.ini ]] ; then
  cp /app/etc/custom-uwsgi.ini /app/uwsgi.ini
fi

if [[ -f /app/etc/resolv.conf ]] ; then
  cp /app/etc/resolv.conf /etc
fi

echo "Starting Webhook MUX service..."

