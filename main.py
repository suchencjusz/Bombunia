import requests
import json
import tiramisu_getter as ciasteczko
import datetime
import time
import os

with open('config.json') as f:
    config = json.load(f)
    f.close()

bombunia_ver="1.0.0-dev"
color=""
debuginfo=""
grades_path = "grades/"
parsedCookies = ""
AllGrades = []
additional_cookie_data = " idBiezacyUczen=4168; idBiezacyDziennik=1485; idBiezacyDziennikPrzedszkole=0; idBiezacyDziennikWychowankowie=0" # z tym problem jest przy tworzeniu setup.py :/
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
    'Referer': 'https://uonetplus-uczen.vulcan.net.pl/powiatchrzanowski/009583/Start', # z tym tezz ale mniejszy 
    'Cookie': '',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1'
}

def SendToDiscord():
    url = config['discord_webhook']

    data = {
        "username" : "Bombunia"
    }

    data["embeds"] = [
        {
            "description" : average+"\n\n"+wiadomoscMotywacyjna+"\n"+"```"+toDiscordWebhook+"```\n"+"_ver: "+bombunia_ver+" _",
            "title" : "Bombunia",
            "color": color
        }
    ] 

    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object

def HowMuchGrades(subject):
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
    temp_limiter = 1
    if CookieCheckONLY() == 200:
        try:
            OpenCookies()
        except:
            ciasteczko.flush()
            ciasteczko.catch()
    else:
        print("Trying again in", (temp_limiter*5), "seconds")
        time.sleep(temp_limiter*5)
        temp_limiter = temp_limiter+1
        ciasteczko.flush()
        ciasteczko.catch()
        GettingCookiesToWORK()

def MuchPalasColor(paly):
    if paly == 0:
        return "65280"
    if paly < 5 and paly != 0:
        return "10479618"
    if paly >= 5 and paly <= 8:
        return "14072585"
    if paly >= 9 and paly <= 12:
        return "16083714"
    if paly > 12:
        return "16711680"

def MuchPalas(paly):
    if paly == 0:
        return "(cud) wpadło ich aż **0** :o"
    if paly < 5 and paly != 0:
        return "Tylko tyle??? wpadło ich: **" + str(paly) + "**"
    if paly >= 5 and paly <= 8:
        return "No mogło wpaść więcej, wpadło ich: **" + str(paly) + "**"
    if paly >= 9 and paly <= 12:
        return "Robi się coraz ciekawiej gagatki, wpadło ich: **" + str(paly) + "**"
    if paly > 12:
        return "Ale z nas to są debile jebane jednak XDDDdd wpadło ich: **" + str(paly) + "**"

GettingCookiesToWORK()
OpenCookies()

r = requests.post(url, data=json.dumps(payload), headers=headers)

try:
    dzejson = r.json()
    print("dlugosc json", len(str(dzejson)))
    if len(str(dzejson)) < 500:
        print("brak uprawnien...")
        ciasteczko.flush()
        ciasteczko.catch()
        r = requests.post(url, data=json.dumps(payload),
                          headers=headers) 
except:
    ciasteczko.catch()
    r = requests.post(url, data=json.dumps(payload), headers=headers)

sumOfAllGrades = 0
muchOfAllGrades = 0

print(dzejson['data'])

for subject in dzejson['data']:
    print(subject['Subject'], "- Brak ocen\n\n") if subject['TableContent'] == None else print(
        subject['Subject'], '-', HowMuchGrades(subject))
    if subject['TableContent'] == None:
        AllGrades.append(
            {'subject_name': subject['Subject'], 'grades': [0,0,0,0,0,0]})
    else:
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
AllGradesToCompare = []
AllGradesFinal.append({'time': dt.timestamp(),
                       'sumOfAllGrades': sumOfAllGrades,
                       'muchOfAllGrades': muchOfAllGrades,
                       'allGrades': AllGrades}
                      )

list = os.listdir(grades_path)
number_files = len(list)

if number_files > 0:
    with open(grades_path + str(number_files) + '.json') as f:
        AllGradesToCompare = json.load(f)
        f.close()
else:
    with open(grades_path + str(number_files+1) + '.json', "w") as f:
        json.dump(AllGradesFinal, f)
        f.close()

changes = False

comparinga = []
comparingb = []

for toCmpr in AllGradesToCompare[0]['allGrades']:
    if toCmpr not in AllGradesFinal[0]['allGrades']:
        changes = True
        comparinga.append(toCmpr)

if changes == False:
    quit()

with open(grades_path + str(number_files+1) + '.json', "w") as f:
    json.dump(AllGradesFinal, f)
    f.close()

for toCmpr in AllGradesFinal[0]['allGrades']:
    if toCmpr not in AllGradesToCompare[0]['allGrades']:
        comparingb.append(toCmpr)

# if len(comparinga) != len(comparingb):
#     print("comprainga != compraingb wtf? ")
#     quit()

newgrades = []

for i in range(len(comparinga)):
    tempciak = [None]*6
    for c in range(6):
        tempciak[c] = int(comparingb[i]['grades'][c]) - int(comparinga[i]['grades'][c])
    newgrades.append({'subject_name': comparinga[i]['subject_name'],
                      'grades': tempciak}
                     )

toDiscordWebhook=""
wiadomoscMotywacyjna=""

sumOfPalas=0

for idx,i in enumerate(newgrades):
    toDiscordWebhook=toDiscordWebhook+i['subject_name']+":\n"
    for idy,y in enumerate(i['grades']):
        if idy == 0:
            sumOfPalas=sumOfPalas+y
        toDiscordWebhook=toDiscordWebhook+str(idy+1)+": "+str(y)+" \n"
    toDiscordWebhook=toDiscordWebhook+"\n"

wiadomoscMotywacyjna = "**Ile dzisiaj wpadło pał?** \n" + MuchPalas(sumOfPalas)
color = MuchPalasColor(sumOfPalas)

print(toDiscordWebhook)

average=""

averageOld=round(AllGradesToCompare[0]['sumOfAllGrades']/AllGradesToCompare[0]['muchOfAllGrades'],5)
averageNew=round(AllGradesFinal[0]['sumOfAllGrades']/AllGradesFinal[0]['muchOfAllGrades'],5)

if averageOld<averageNew:
    average = "Nasza średnia wzrosła z "
else:
    average = "Nasza średnia spadła z "

average += str(averageOld)+" do "+str(averageNew)+" (średnia nie uwzględnia wag)"

print(average)

if config["discord_webhook_f"] == True: SendToDiscord()