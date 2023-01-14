#!/bin/bash

for apps in output/results/*; do
	printf "%s\n" "${apps##*/}"
	for regex in $apps/*; do

		if [ ${regex##*/} == "all_links.txt" ]; then
			:
		elif [[ ${regex##*/} =~ AIza\[0\-9A\-Za\-z\\\\-\_\]\{35\}\.txt ]]; then
			while IFS= read -r key; do
				sleep 1
				if [ $(curl -s -o /dev/null -w "%{http_code}" "https://www.google.com/maps/embed/v1/place?q=london&key=""$key") == 200 ]; then
					printf "working maps: %s\n" "$key"
				fi
				sleep 1
				if [ $(curl -s "https://maps.googleapis.com/maps/api/directions/json?origin=Geneva&destination=Zurich&key=""$key" | jq --raw-output '.status') == "OK" ]; then
					printf "working directions: %s\n" "$key"
				fi
				sleep 1
				if [ $(curl -s "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key=""$key" | jq --raw-output '.status') == "OK" ]; then
					printf "working elevation: %s\n" "$key"
				fi

			done <$regex
		else
			:
		fi

	done
done
