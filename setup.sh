#!/bin/bash

read -p "Enter your Publish Key: " pub_key
echo "PN_PUB_KEY=$pub_key" >> .env

read -p "Enter your Subscribe Key: " sub_key
echo "PN_SUB_KEY=$sub_key" >> .env

read -p "Enter your Name: " name
echo "NAME=$name" >> .env