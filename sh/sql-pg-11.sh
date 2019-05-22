#! /bin/bash

gcloud beta sql instances create hm2-pg \
       --database-version=POSTGRES_11 \
       --root-password=shii,Rah6c \
       --zone=europe-west4-a \
       --tier=db-f1-micro
