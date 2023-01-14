#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import cloudscraper
import sys
import warnings
from pathlib import Path
import os
from tqdm import tqdm
import signal
from random import randint
from time import sleep

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def cycle():
    with open('output/playids/android.txt') as f:
        lines = f.read().splitlines()
        for line in lines:
            get_apk(line)
    

def get_apk(app_name):
    print("getting download link for %s" %(app_name))
    site = "https://apkpure.com"
    url = "https://apkpure.com/search?q=%s" %(app_name)
    scraper1 = cloudscraper.create_scraper(interpreter='nodejs', recaptcha={
        'provider': 'anticaptcha',
        'api_key': 'ANTICAPTCHA_TOKEN_HERE'
    })
    proxy = "PROXY_IP_HERE"
    port = "PROXY_PORT_HERE"
    proxies = {
        "http": proxy + ':' + port,
        "https": proxy + ':' + port
    }
    print('CHECKING IP')
    try:
        checker = scraper1.get('https://iphelper.now.sh',proxies=proxies)
    except:
        print('FAILED')
        quit()
    if checker.status_code == 403 or checker.status_code == 503 :
        print("IP ratelimited")
    if checker.text == "YOUR_IP_HERE":
        quit()
    else:
        print(checker.text)
    sleep(1)
    html = scraper1.get(url,proxies=proxies)
    parse = BeautifulSoup(html.text, "html.parser")
    if parse.find("div",class_="search-empty") is not None:
        print("no search results for id")
        return
    i = parse.find("p",class_='search-title')
    i = i.find("a")
    
    a_url = i["href"]
    if a_url.rsplit('/', 1)[1] != app_name :
        print('Id not found in search results')
        return
    Path("output/apks/" + app_name).mkdir(parents=True, exist_ok=True)
    app_url = site + a_url + "/versions"
    sleep(randint(2,5))
    html2 = scraper1.get(app_url,proxies=proxies)
    if html2.status_code == 410:
        print('no versions page, exiting loop')
        return
    parse2 = BeautifulSoup(html2.text, "html.parser")
    versions = parse2.find("div", class_='ver')
    if versions is None:
        print('no downloads found, bad')
        return
    downloads = versions.find_all("li")
    for item in downloads:
        down = item.find("a", class_='down')
        if down:
            download_link = site + down["href"]
            version = item.find("span",class_='ver-item-n').contents
            xapk = True if item.find("span",class_="ver-xapk") else False
            download_apk(scraper1, proxies, app_name, version[0], download_link, xapk, False, 0)
        else:
            variantlink = item.find("a")
            sleep(randint(2,5))
            variantspage = scraper1.get(site + variantlink["href"],proxies=proxies)
            anothersoup = BeautifulSoup(variantspage.text, "html.parser")
            properlink = anothersoup.find("div", class_="left").select("a[href*=download][href*=variants]")
                
            variantn = 1
            for variant in properlink:
                download_link = site + variant["href"]
                
                version = item.find("span",class_='ver-item-n').contents
                xapk = True if item.find("span",class_="ver-xapk") else False
                download_apk(scraper1, proxies, app_name, version[0], download_link, xapk, True, variantn)
                variantn += 1

def download_apk(scraper1, proxies, app_name, version, download_link, xapk, variant, variantn):
    print("downloading %s %s" %(app_name, version))
    
    if variant == False:
        sleep(randint(2,5))
        x = scraper1.get(download_link,proxies=proxies)
        soup = BeautifulSoup(x.text, "html.parser")
        link = soup.find("a",id="download_link")
        
        output_file = "output/apks/" + app_name + "/" + version + (".xapk" if xapk else ".apk")
        downloader(scraper1, proxies, link["href"], output_file)

    else:
        print('downloading variant ' + str(variantn))
        sleep(randint(2,5))
        x = scraper1.get(download_link,proxies=proxies)
        soup = BeautifulSoup(x.text, "html.parser")
        link = soup.find("a",id="download_link")
        
        output_file = "output/apks/" + app_name + "/" + version + '-v' + str(variantn) + (".xapk" if xapk else ".apk")
        downloader(scraper1, proxies, link["href"], output_file)
        
    
def downloader(scraper1, proxies, link, output_file, tries=1):
    if os.path.exists(output_file):
            print("file exists, skipping with no size check")
            return
    try:
        sleep(randint(2,5))
        r = scraper1.get(link,proxies=proxies,stream=True)
        
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024 #1 Kibibyte
        
        if os.path.exists(output_file) and os.path.getsize(output_file) == total_size:
            print("already exists, skipping")
            return
        elif os.path.exists(output_file):
            print("incomplete exists, deleting")
            os.remove(output_file)
        
        t=tqdm(total=total_size, unit='iB', unit_scale=True)
        
        with open(output_file, 'wb') as f:
            if total_size is None: # no content length header
                f.write(r.content)
            else:
                for data in r.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
        t.close()
        if total_size != 0 and t.n != total_size:
            print("something went wrong")
            print("deleting")
            os.remove(output_file)
            if tries == 3:
                print("failed 3 tries, skipping")
                return
            print("retrying")
            downloader(scraper1, proxies, link, output_file, tries+1)
        else:
            print("done")
            
    except KeyboardInterrupt:
        os.remove(output_file)
        sys.exit(130)

def main(args):
    cycle()

if __name__ == "__main__":
    main(args=sys.argv)
