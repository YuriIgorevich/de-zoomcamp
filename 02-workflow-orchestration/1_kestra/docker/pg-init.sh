#!/bin/bash
function create_db() {
    local db=$1
    
    [ -z  $db ] && { echo "No db provided. Skipping."; return; }
    
    local command="CREATE DATABASE $db"
    echo "Creating database $db"
    psql \
        --username $POSTGRES_USER \
        --set ON_ERROR_STOP=1 \
        --quiet \
        --command "$command" 
}

function create_user() {
    local user=$1
    local password=$2
    local command="CREATE USER $user"

    [ -z  $user ] && { echo "No user provided. Skipping."; return; }
    
    if [ ! -z $password ] ;
    then 
        command="$command WITH PASSWORD '$password'"
    fi

    echo "Creating user $user"
    psql \
        --username $POSTGRES_USER \
        --set ON_ERROR_STOP=1 \
        --quiet \
        --command "$command"
}

function grant_privs_to_user() {
    local db=$1
    local user=$2

    [ -z  $db ] || [ -z  $user ] && { echo "No db/user provided. Skipping."; return; }

    command_1="GRANT ALL PRIVILEGES ON DATABASE $db TO $user"
    command_2="ALTER DATABASE $db OWNER TO $user"
    echo "Granting privileges on db $db to user $user"
    psql \
        --username $POSTGRES_USER \
        --dbname $KESTRA_DB \
        --set ON_ERROR_STOP=1 \
        --quiet \
        --command "$command_1" \
        --command "$command_2"
}

function init_db() {
    local db="${1:-}"
    local user="${2:-}"
    local password="${3:-}"

    create_db $db
    create_user $user $password
    grant_privs_to_user $db $user
}


init_db $KESTRA_DB $KESTRA_USER $KESTRA_PASSWORD
