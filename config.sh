#!/usr/bin/env bash
# RECSYS_HOME="/home/ubuntu/corvus"
RECSYS_HOME="/home/vu/projects/Lina/src"
# RECSYS_HOME="/home/ubuntu/Lina"
PG_ENDPOINT="rdscat.zalora.com"
PG_USER="admin_ds"
PG_DB="ds"
PG_PORT="5432"
today="$(date '+%Y%m%d')"
safe_psql_footer_off () {
    while ! psql -P footer=off -A -F$'\t' -h $PG_ENDPOINT -U $PG_USER -d $PG_DB -p $PG_PORT -c "$1"; do
        # output to stderr
        echo "Something went wrong when getting Data from rdscat, retry in 5s" >&2
        sleep 5s
    done
}

safe_psql () {
    while ! psql -t -A -F$'\t' -h $PG_ENDPOINT -U $PG_USER -d $PG_DB -p $PG_PORT -c "$1"; do
        # output to stderr
        echo "Something went wrong when getting Data from rdscat, retry in 5s" >&2
        sleep 5s
    done
}

safe_psql_footer_off_large_result () {
    while ! psql --variable=FETCH_COUNT=500000 -P footer=off -A -F$'\t' -h $PG_ENDPOINT -U $PG_USER -d $PG_DB -p $PG_PORT -c "$1"; do
        # output to stderr
        echo "Something went wrong when getting Data from rdscat, retry in 5s" >&2
        sleep 5s
    done
}
