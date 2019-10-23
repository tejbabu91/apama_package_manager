#!/bin/bash

for i in $(ls *.zip)
do
	curl -H "Content-Type:application/octet-stream" --data-binary "@$i" http://127.0.0.1:5000/packages
done
