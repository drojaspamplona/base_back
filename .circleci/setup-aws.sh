#!/bin/bash
mkdir ~/.aws
printf "[profile eb-cli]\naws_access_key_id = ${AWS_ACCESS_KEY_ID}\naws_secret_access_key = ${AWS_SECRET_ACCESS_KEY}" > ~/.aws/config
