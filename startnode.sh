#!/usr/bin/env bash
java -jar /home/ubuntu/selenium-server-standalone-2.26.0.jar -role node -hub http://50.17.215.201:80/grid/register -browser browserName=firefox