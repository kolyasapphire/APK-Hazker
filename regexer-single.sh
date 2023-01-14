#!/bin/bash

name=$1
folder=$2
links="output/results/$name/all_links.txt"
keys="output/results/$name/all_keys.txt"
keysfolder="output/results/$name"

if [ -z "$(ls -A $folder)" ]; then
    echo "empty apk folder, skipping"
    exit
fi

regxlinks () {
    mkdir -p "$keysfolder"
    
    ag -ro --nofilename --nobreak "[\"'\`](https?://|/)[\w\.-/]+[\"'\`]" "$folder" > "$links"
    
    gsed -i "/^$/d" "$links"
    gsed -i "s/'//g" "$links"
    gsed -i 's/"//g' "$links"
    
    sort -u -o "$links" "$links"
    
}

regxkeys () {
    for line in `cat config/key_regex.txt`; do
        printf "doing regex %s\n" "$line"
        
        mkdir -p "$keysfolder"
        
        ag -or --nofilename --nobreak "$line" "$folder" > "$keysfolder/$line.txt"
        
        if [ -s "$keysfolder/$line.txt" ] ; then
            echo "Found stuff - Sorting"
            
            gsed -i "/^$/d" "$keysfolder/$line.txt"
            sort -u -o "$keysfolder/$line.txt" "$keysfolder/$line.txt"
            
        else
            echo "Nothing found, deleting"
            rm "$keysfolder/$line.txt"  
        fi
        
        printf "finished regex %s\n" "$line"
    done
}

echo "Extracting endpoints"
regxlinks
echo "Endpoints saved"

echo "Extracting keys"
regxkeys
echo "Keys saved"
