#! /bin/bash

if test "$1" == ""; then
    echo "Error: missing name of instance"
    exit
fi

gcloud beta sql instances create "$1" \
       --database-version=POSTGRES_11 \
       --root-password=shii,Rah6c \
       --zone=europe-west4-a \
       --tier=db-f1-micro
