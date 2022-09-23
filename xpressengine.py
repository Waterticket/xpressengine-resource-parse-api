import csv
import os
from selenium import webdriver
#selenium 웹브라우저 조작 자동화 SW

from bs4 import BeautifulSoup
driver = webdriver.Chrome("C:\chromedriver.exe")
import time

from PIL import Image
from PIL import UnidentifiedImageError
import requests

cnt = 0
packageData = []
f = open('rx_autoinstall_packages.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
for line in rdr:
    if line[0] == "package_srl":
        continue

    package_srl = line[0]
    cnt += 1

    if(cnt <= 800):
        continue

    print("============================================================")
    print("Count :", cnt)
    print("PackageSrl: ", package_srl)

    wd.get("https://xe1.xpressengine.com/index.php?mid=download&package_id="+package_srl)
    html = driver.page_source
    soupCB = BeautifulSoup(html, 'html.parser')

    SmallVar = soupCB.select("small")[0].get_text()

    ScreenShots = soupCB.select("div.gallery img.thumbnail")
    ScreenShotNum = 0
    ScreenShotArr = []
    for screenshot in ScreenShots:
        if not os.path.isdir('screenshot/'+str(package_srl)):
            os.mkdir('screenshot/'+str(package_srl))

        print("screenshot", screenshot['src'])
        ScreenShotNum += 1

        try:
            img_res = requests.get(screenshot['src'], stream=True)
            if img_res.status_code != 200:
                print("HTTP Error", img_res.status_code)
                continue

            img = Image.open(img_res.raw)
            img.save('screenshot/'+str(package_srl)+'/'+str(ScreenShotNum)+"."+img.format.lower())
            ImagePath = str(ScreenShotNum) + "." + img.format.lower()
            ScreenShotArr.append(ImagePath)
        except requests.exceptions.HTTPError as errb:
            print("Http Error : ", errb)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting : ", errc)
        except requests.exceptions.HTTPError as errb:
            print("Http Error : ", errb)
        except requests.exceptions.RequestException as erra:
            print("AnyException : ", erra)
        except UnidentifiedImageError as erra:
            print("ImageException : ", erra)

    Spec = soupCB.select(".panel-body._viewer")[0]
    DocumentImage = Spec.select("img")

    docImageNum = 0
    docImageArr = []
    for documentImg in DocumentImage:
        if not os.path.isdir('docimage/' + str(package_srl)):
            os.mkdir('docimage/' + str(package_srl))

        print("docimage", documentImg['src'])
        docImageNum += 1

        try:
            img_res = requests.get(documentImg['src'], stream=True)
            if img_res.status_code != 200:
                print("HTTP Error", img_res.status_code)
                continue

            img = Image.open(img_res.raw)
            img.save('docimage/' + str(package_srl) + '/' + str(docImageNum) + "." + img.format.lower())
            ImagePath = str(docImageNum) + "." + img.format.lower()
            docImageArr.append(ImagePath)
            documentImg['src'] = 'https://rhymix.repo.hoto.dev/files/attach/oldxe/docimage/' + str(package_srl) + '/' + ImagePath
        except requests.exceptions.HTTPError as errb:
            print("Http Error : ", errb)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting : ", errc)
        except requests.exceptions.HTTPError as errb:
            print("Http Error : ", errb)
        except requests.exceptions.RequestException as erra:
            print("AnyException : ", erra)
        except UnidentifiedImageError as erra:
            print("ImageException : ", erra)

    DocumentHTML = str(Spec)

    packageInfo = {
        "PackageSrl": int(package_srl),
        "ScreenShots": ScreenShotArr,
        "DocumentImg": docImageArr,
        "DocumentHTML": DocumentHTML,
    }
    print(packageInfo)

    packageData.append(packageInfo)
    time.sleep(1)

    if cnt % 100 == 0:
        import json
        with open("packageDoc-"+str(cnt)+".json", "w", encoding="utf-8") as json_file:
            json.dump(packageData, json_file, ensure_ascii=False)
        print("Part saved.")
        packageData.clear()

    print('\n')
f.close()

import json
with open("packageDoc-last.json", "w", encoding="utf-8") as json_file:
    json.dump(packageData, json_file, ensure_ascii=False)
