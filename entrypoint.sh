#!/usr/bin/env bash

# wait for postgress to start
until /usr/bin/env python pg_ping.py 2>&1 >/dev/null; do
	echo 'wait for postgres to start...'
	sleep 5
done

if [ ! -f "/opt/init/.done" ]; then
    /usr/bin/env python -u /usr/local/bin/otree resetdb --noinput -v 1 \
    && touch /opt/init/.done
fi

/usr/local/bin/forego start -f /Procfile
