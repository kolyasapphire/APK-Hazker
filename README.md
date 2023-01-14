# APK Hazker

Automated suite for HackerOne scope APK downloading, decompilation and regex searching for secrets.

## Intro

This project was done a long time ago, code is rough and things can be broken.

Open sourcing the code as an example, hopefully gives some inspiration to security researchers.

## Dependencies

1. Install python requirements.txt
2. Install The Silver Searcher https://github.com/ggreer/the_silver_searcher
3. Make sure to have apktool installed
4. Make sure to have nodejs for html interpretation

## Setup

1. In h1.py fill in anticaptcha api key if needed
2. In h1.py fill in your proxy ip
3. In h1.py fill in your ip for a killswitch
4. `python3 h1.py`
5. `python3 apk-down.py`
6. ./decompile.sh

## Suggestions

To sync output from server better use rsync:
`rsync -azP root@1.2.3.4:/root/apk-hazker/output/sources/ tmp.nosync.noindex/sources`

APK files can be huge, invest in cheap external storage and set up a symlink `apks` in `output`.
