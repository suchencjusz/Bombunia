import requests
import json
import tiramisu_getter as ciasteczko

with open('config.json') as f:
    config = json.load(f)

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


def getCookies():
    pdCookies, cookieJsonData = "", ""
    with open('cookies.json') as f:
        cookieJsonData = json.load(f)
    for idx, i in enumerate(cookieJsonData):
        pdCookies = pdCookies + i['name']+"="+i['value']
        if idx != len(cookieJsonData)-1:
            pdCookies = pdCookies + "; "
    return pdCookies


def MuchiosAmogisGrades(subject):
    sum = 0
    for i in subject['ClassSeries']['Items']:
        sum = sum+i['Value']
    return sum

def LoadCookie():
    try:
        parsedCookies = getCookies()
    except:
        ciasteczko.catch()
        parsedCookies = getCookies()

def CookieCheck():
    limiter = 0
    rn = requests.post(url, data=json.dumps(payload), headers=headers)
    while rn.status_code != 200 and limiter < 4:
        print(rn.status_code, " <code of vulcan request")
        ciasteczko.flush()
        ciasteczko.catch()
        LoadCookie()
        rn = requests.post(url, data=json.dumps(payload),
                           headers=headers)  # grades request
        limiter = limiter + 1

    if limiter > 3:  # raz dziala, raz nie tak jak wyzej czy tam nizej z try catch
        print("Limiter loop exceeded")
        CookieCheck()
        limiter = 0

    return rn


def GradesToList(subject):
    grades_return = []
    for i in range(0, 6, 1):
        grades_return.append(
            int(subject['ClassSeries']['Items'][5-i]['Value']))
    return grades_return


LoadCookie()

headers['Cookie'] = parsedCookies + additional_cookie_data

r = CookieCheck()

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

print(round(sumOfAllGrades/muchOfAllGrades, 2),
      "uwaga średnia klasy nie uwzględnia wag!")

for i in AllGrades:
    print(i)