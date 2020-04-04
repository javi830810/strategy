#!/bin/bash

$pwd

#Start remote deploy
echo "Starting remote deploy"

echo "Creating Login information"
mkdir -p ~/.ssh
eval `ssh-agent -s`

echo "Creating private Key"
echo "$STRATEGY_PK" >> ~/.ssh/strategy.pk
chmod 600 ~/.ssh/strategy.pk
ssh-add ~/.ssh/strategy.pk

echo "Copying sensitive variables to Server"
scp -i ~/.ssh/strategy.pk deploy.sh $DEPLOY_USER@$SERVER:/root/strategy

ssh -i ~/.ssh/strategy.pk $DEPLOY_USER@$SERVER 'bash -s' < deploy.sh

echo "Finishing deploy"