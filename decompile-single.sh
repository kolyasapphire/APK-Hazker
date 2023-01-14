#!/bin/bash

app=$1
app=${app##*/}
version=$2
version=${version##*/}

versionnodot=${version%.apk*}
versionnodot=${version%.xapk*}
pathnodot=output/apks/$app/$versionnodot

path=output/apks/$app/$version
xapkversion=${version##-}
xapkpath=output/apks/$app/$xapkversion

output=output/sources/$app/$versionnodot

if [[ $(df -g "output/sources" | awk 'NR==2 { print $4 }') < 10 ]]; then
    echo "no space"
    exit 1
fi

[ -d $output ] && "already exists, moving on" && exit

if ! type "apktool" &> /dev/null; then
    echo "No apktool installed."
    exit
fi

extract () {
    if [[ $version == *".apk" ]]; then
        echo "its an apk"
        apktool d "$path" -o "$output" -f -q
        echo "decompiled"
    elif [[ $version == *".xapk" ]]; then
        echo "its a xapk"
        unzip -q "$path" -d "$pathnodot"
        echo "unzipped"
        apktool d "$pathnodot/$app.apk" -o "$output" -f -q
        echo "decompiled"
        echo "cleaning zip folder"
        rm -rf "$pathnodot"
        echo "cleaned"
    else
        printf 'file not found:\n'
        printf "%s \n" "$path"
    fi
}

printf "Decompiling %s %s \n" "$app" "$version"
extract
printf "Decompiled! GB left: %s\n" "$(df -g "output/sources" | awk 'NR==2 { print $4 }')"
exit
