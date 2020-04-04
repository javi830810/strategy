#!/bin/bash

pwd

#Start remote deploy
echo "Starting remote deploy"

echo "Creating Login information"
mkdir -p ~/.ssh
eval `ssh-agent -s`

echo "Disabling fingerprint check"
ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" $DEPLOY_USER@$SERVER

echo "Creating private Key"
echo "$STRATEGY_PK" | base64 --decode > ~/.ssh/strategy.pk
chmod 400 ~/.ssh/strategy.pk

echo "Executing script on Server"
ssh -i ~/.ssh/strategy.pk $DEPLOY_USER@$SERVER 'bash -s' < ./scripts/deploy.sh

echo "Finishing deploy"