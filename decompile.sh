#!/bin/bash

if ! type "apktool" &> /dev/null; then
    echo "No apktool installed."
    exit
fi

# while IFS= read -r app; do
apps=$(ls output/apks/ | wc -l | tr -d ' ')
printf "%s apps to process\n" "$apps"
appn=1
for app in output/apks/*; do
    printf "%s/%s\n" "$appn" "$apps"
    appn=$(($appn+1))
    printf "starting working on %s \n" "${app##*/}"
    
    if [ -d output/results/${app##*/} ]; then
        echo "results folder already exists, moving on"
        continue
    fi
    
    versions=$(ls $app | wc -l | tr -d ' ')
    printf "%s versions to process\n" "$versions"
    versionn=1
    for version in $app/*; do
        printf "%s/%s\n" "$versionn" "$versions"
        versionn=$(($versionn+1))
        printf "doing version %s \n" "${version##*/}"
        
        if [[ $version != *".apk" && $version != *".xapk" ]]; then
            printf "invalid extension or no items for %s - skipping\n" "$version"
            continue
        fi
        
        ./decompile-single.sh "$app" "$version"
    done

    printf "starting regex %s\n" "${app##*/}" 
    ./regexer-single.sh "${app##*/}" "output/sources/${app##*/}"
    printf "finished regex %s\n" "${app##*/}"
    
    # echo "starting cleaning sources"
    # rm -rf "output/sources/${app##*/}"
    # echo "finished cleaning sources"

    # printf "cleaning apks for %s \n" "$app"
    # rm -rf "output/apks/$app"
    # printf "cleaning done \n"
 
done  
