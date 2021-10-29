import json

email = input("Enter email: ")
password = input("Enter password: ")
school_url = input("Enter school URL: ")
discord_webhook = input("Enter discord webhook URL: ")

result = {'email': email,
          'password': password,
          'school_url': school_url,
          'discord_webhook': discord_webhook}

with open('config.json', "w") as f:
    json.dump(result, f)
    f.close()