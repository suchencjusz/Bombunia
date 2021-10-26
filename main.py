import requests
import json
import tiramisu_getter as ciasteczko
import datetime
import time
import os

with open('config.json') as f:
    config = json.load(f)
    f.close()

grades_path = "grades/"
parsedCookies = ""
AllGrades = []
additional_cookie_data = " idBiezacyUczen=4168; idBiezacyDziennik=1485; idBiezacyDziennikPrzedszkole=0; idBiezacyDziennikWychowankowie=0"
url = 'https://uonetplus-uczen.vulcan.net.pl/powiatchrzanowski/009583/Statystyki.mvc/GetOcenyCzastkowe'
payload = {
    'idOkres': 1045
}
headers = {
    'Host': 'uonetplus-uczen.vulcan.net.pl',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
    'Accept': '*/*',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-V-RequestVerificationToken': '0rcpQv4ZNqZi_MLZY-u0wVKTJuTseNSfXpx5s6SMDjcendZVfuhc7LcMN4e2ZMwDVUolfSWp7F-dZWeb2xHIr1KrsK6rbsvKwHWCwsVleOqYOi0D0',
    'X-V-AppGuid': 'fc21b3089d2d9dc61c1cc83e6e382576',
    'X-V-AppVersion': '21.10.0010.47230',
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '16',
    'Origin': 'https://uonetplus-uczen.vulcan.net.pl',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://uonetplus-uczen.vulcan.net.pl/powiatchrzanowski/009583/Start',
    'Cookie': '',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1'
}


def MuchiosAmogisGrades(subject):
    sum = 0
    for i in subject['ClassSeries']['Items']:
        sum = sum+i['Value']
    return sum


def GradesToList(subject):
    grades_return = []
    for i in range(0, 6, 1):
        grades_return.append(
            int(subject['ClassSeries']['Items'][5-i]['Value']))
    return grades_return


def OpenCookies():
    pdCookies, cookieJsonData = "", ""
    if os.path.isfile('cookies.json') and os.path.getsize('cookies.json') != 0:
        with open('cookies.json') as f:
            cookieJsonData = json.load(f)
        for idx, i in enumerate(cookieJsonData):
            pdCookies = pdCookies + i['name']+"="+i['value']
            if idx != len(cookieJsonData)-1:
                pdCookies = pdCookies + "; "
        headers['Cookie'] = pdCookies + additional_cookie_data
    else:
        ciasteczko.flush()
        ciasteczko.catch()


def CookieCheckONLY():
    OpenCookies()
    rn = requests.post(url, data=json.dumps(payload), headers=headers)
    return rn.status_code


def GettingCookiesToWORK():
    temp_limiter=1
    if CookieCheckONLY() == 200:
        try:
            OpenCookies()
        except:
            ciasteczko.flush()
            ciasteczko.catch()
    else:
        print("Trying again in",(temp_limiter*5),"seconds")
        time.sleep(temp_limiter*5)
        temp_limiter=temp_limiter+1
        ciasteczko.flush()
        ciasteczko.catch()
        GettingCookiesToWORK()


GettingCookiesToWORK()
OpenCookies()

r = requests.post(url, data=json.dumps(payload), headers=headers)

try:
    dzejson = r.json()
    print("dlugosc json", len(str(dzejson)))
    if len(str(dzejson)) < 500:
        print("chuj")
        ciasteczko.catch()
except:
    ciasteczko.catch()

sumOfAllGrades = 0
muchOfAllGrades = 0

print(dzejson['data'])

for subject in dzejson['data']:
    print(subject['Subject'], "- Brak ocen\n\n") if subject['TableContent'] == None else print(
        subject['Subject'], '-', MuchiosAmogisGrades(subject))
    if subject['TableContent'] != None:
        AllGrades.append(
            {'subject_name': subject['Subject'], 'grades': GradesToList(subject)})

        for idx, label in enumerate(subject['ClassSeries']['Items']):
            sumOfAllGrades = sumOfAllGrades+(int(label['Value'])*(6-idx))
            muchOfAllGrades = muchOfAllGrades+label['Value']
            print("Ocen \'"+str(6 - idx)+"\':", label['Value'], end="\n")
            print("\n") if idx == 5 else None

print(round(sumOfAllGrades/muchOfAllGrades, 5),
      "uwaga średnia klasy nie uwzględnia wag!")

dt = datetime.datetime.now()

AllGradesFinal = []
AllGradesFinal.append({'time': str(dt.isoformat()),
                       'sumOfAllGrades': sumOfAllGrades,
                       'muchOfAllGrades': muchOfAllGrades,
                       'grades': AllGrades}
                      )

with open(f'{grades_path}t.json', "w") as f:
    json.dump(AllGradesFinal, f)
    f.close()