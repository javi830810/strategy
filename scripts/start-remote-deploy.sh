#!/bin/bash

pwd

#Start remote deploy
echo "Starting remote deploy"

echo "Creating Login information"
mkdir -p ~/.ssh
eval `ssh-agent -s`

echo "Creating private Key"
echo "$STRATEGY_PK" | base64 --decode > ~/.ssh/strategy.pk
chmod 400 ~/.ssh/strategy.pk

echo "Executing script on Server"
ssh -i ~/.ssh/strategy.pk -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $DEPLOY_USER@$SERVER 'bash -s' < ./scripts/deploy.sh

echo "Finishing deploy"