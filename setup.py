import json

email = input("Email konta vulcan: ")
password = input("Haslo konta vulcan: ")
school_url = input("Adres szkoly dziennika vulcan: ")
discord_webhook_f = input("Discord webhook t/n: ")
api_key_imgur = input("Imgur api key: ")
client_imgur = input("Imgur client id: ")

if discord_webhook_f.lower() == "t":
    discord_webhook_f = True
    discord_webhook = input("Discord webhook URL: ")
else:
    discord_webhook_f = False
    discord_webhook = ""

result = {'email': email,
          'password': password,
          'school_url': school_url,
          'discord_webhook': discord_webhook,
          'discord_webhook_f': discord_webhook_f,
          'api_key_imgur': api_key_imgur,
          'client_imgur': client_imgur}

with open('config.json', "w") as f:
    json.dump(result, f)
    f.close()