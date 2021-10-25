import requests
import json

email = input("Enter email: ")
password = input("Enter password: ")
school_url = input("Enter school URL: ")

for i in ('email','password','school_url'):
    data = locals()[i]

with open('config.json', "w") as f: 
    json.dump(email,password,school_url,f)