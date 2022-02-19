#!/bin/bash

set -e

PRE_START=/app/prestart.bash
if [ -f $PRE_START ] ; then
    echo "Running script $PRE_START_PATH"
    . $PRE_PRE_START
fi

# Sometimes /etc/resolv.conf does not get passed correctly into container
if [ -f /app/etc/resolv.conf ] ; then
    cp /app/etc/resolv.conf /etc
fi

# Start Supervisor, with Nginx and uWSGI
exec /usr/bin/supervisord -c /etc/supervisor/supervisord.conf

