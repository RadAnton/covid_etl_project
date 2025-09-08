#!/bin/sh
set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD=secret123 psql -h "$host" -U antonradchenko -d covid_db -c '\q'; do
  >&2 echo "Waiting for Postgres..."
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
