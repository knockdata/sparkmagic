#!/bin/bash

set -ex

if [ -n "$LIVY_ENDPOINT" ]; then
    sed -i "s|http://localhost:8998|$LIVY_ENDPOINT|g" /home/$NB_USER/.sparkmagic/config.json
fi

if [ -n "$SPARK_S3_BUCKET" ]; then
    sed -i "s|s3a_bucket|$SPARK_S3_BUCKET|g" /home/$NB_USER/.sparkmagic/config.json
fi

if [ -n "$SPARK_S3_ACCESS_KEY" ]; then
    sed -i "s|s3a_access_key|$SPARK_S3_ACCESS_KEY|g" /home/$NB_USER/.sparkmagic/config.json
fi

if [ -n "$SPARK_S3_SECRET_KEY" ]; then
    sed -i "s|s3a_secret_key|$SPARK_S3_SECRET_KEY|g" /home/$NB_USER/.sparkmagic/config.json
fi

if [ -n "$JUPYTERHUB_USER" ]; then
    sed -i "s|owner_name|$JUPYTERHUB_USER|g" /home/$NB_USER/.sparkmagic/config.json
fi

exec jupyterhub-singleuser "$@"
